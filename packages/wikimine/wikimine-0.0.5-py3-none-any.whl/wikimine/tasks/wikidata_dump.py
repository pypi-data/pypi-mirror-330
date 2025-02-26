import bz2
import gzip
import json
from dataclasses import dataclass
from tqdm import tqdm
from cmfn import listdir

from playhouse.sqlite_ext import *

from wikimine.db import (
    WikidataEntityEnSiteLink,
    WikidataEntityLabel,
    WikidataEntityDescriptions,
    WikidataEntityAliases,
    WikidataClaim, db_proxy
)


def smart_open(file_path, mode='r'):
    """
    :param file_path: Path to the file to be open.
    :param mode: The mode in which the file should be opened. Default is 'r'.
    :return: The file object for reading or writing.
    """
    if file_path.endswith('.gz'):
        return gzip.open(file_path, mode + 't') if 'b' not in mode else gzip.open(file_path, mode)
    elif file_path.endswith('.bz2'):
        return bz2.open(file_path, mode + 't') if 'b' not in mode else bz2.open(file_path, mode)
    else:
        return open(file_path, mode)


def iter_jsonl(fn):
    """
    :param fn: The file path of the JSONL file to be read
    :return: A generator object that yields each valid JSON object from the file
    """
    with smart_open(fn) as fd:
        for line in fd:
            line = line.strip()
            if line:
                yield json.loads(line)


@dataclass
class ProcessedEntity:
    entity_id: str
    site_link: WikidataEntityEnSiteLink
    labels: list[WikidataEntityLabel]
    descriptions: list[WikidataEntityDescriptions]
    aliases: list[WikidataEntityAliases]
    claims: list[WikidataClaim]


def get_target_id(mainsnak):
    target_entity = None
    if 'datavalue' in mainsnak:
        datavalue = mainsnak['datavalue']
        if datavalue.get('type') == 'wikibase-entityid':
            target_entity = datavalue.get('value', {}).get('id')
    return target_entity


def process_entity(
        entity_dict,
        process_labels=True,
        process_desc=True,
        process_aliases=True,
        process_claims=True
) -> ProcessedEntity:
    """
    process one line of wikidata json dump
    :param entity_dict:
    :return:
    """
    entity_id = entity_dict['id']
    site_link = None

    if entity_dict.get("sitelinks", {}).get("enwiki", {}).get("title", None) is not None:
        site_link = WikidataEntityEnSiteLink(
            entity_id=entity_id,
            title=entity_dict["sitelinks"]['enwiki']['title']
        )

    # Extract labels
    labels = [
        WikidataEntityLabel(
            entity_id=entity_id,
            language=lang,
            value=label_info['value']
        ) for lang, label_info in entity_dict.get('labels', {}).items()
    ] if process_labels else []

    # Extract descriptions
    descriptions = [
        WikidataEntityDescriptions(
            entity_id=entity_id,
            language=lang,
            value=desc_info['value']
        ) for lang, desc_info in entity_dict.get('descriptions', {}).items()
    ] if process_desc else []

    # Extract aliases
    aliases = [
        WikidataEntityAliases(
            entity_id=entity_id,
            language=lang,
            value=alias_info['value']
        ) for lang, alias_list in entity_dict.get('aliases', {}).items()
        for alias_info in alias_list
    ] if process_aliases else []

    # Extract claims
    claims = []

    if process_claims:
        for property_id, claim_list in entity_dict.get('claims', {}).items():
            # if property_id not in ['P279', 'P31']:
            #     continue

            for claim in claim_list:

                if claim['rank'] == 'deprecated':
                    continue

                mainsnak = claim.get('mainsnak', {})
                target_entity = get_target_id(mainsnak)

                claims.append(
                    WikidataClaim(
                        source_entity=entity_id,
                        property_id=property_id,
                        body=claim,
                        target_entity=target_entity
                    )
                )

    return ProcessedEntity(
        entity_id=entity_id,
        site_link=site_link,
        labels=labels,
        descriptions=descriptions,
        aliases=aliases,
        claims=claims
    )


def has_english_wikipedia_link(entity):
    sitelinks = entity.get("sitelinks", {})
    return "enwiki" in sitelinks


def has_english_label(entity):
    labels = entity.get("labels", {})
    return "en" in labels


def flatten_batch(batch: list[ProcessedEntity]) -> list[WikidataEntityLabel]:
    labels = []
    descriptions = []
    aliases = []
    claims = []
    site_links = []

    for entity in batch:
        labels.extend(entity.labels)
        descriptions.extend(entity.descriptions)
        aliases.extend(entity.aliases)
        claims.extend(entity.claims)
        if entity.site_link:
            site_links.append(entity.site_link)

    return labels, descriptions, aliases, claims, site_links


def insert_wikidata_batch(batch_results, batch_size):
    labels, descriptions, aliases, claims, site_links = flatten_batch(batch_results)
    WikidataEntityLabel.bulk_create(labels, batch_size)
    WikidataEntityDescriptions.bulk_create(descriptions, batch_size)
    WikidataEntityAliases.bulk_create(aliases, batch_size)
    WikidataClaim.bulk_create(claims, batch_size)
    WikidataEntityEnSiteLink.bulk_create(site_links, batch_size)


def add_wikidata_dump_folder(dump_folder, batch_size=5000, dry_run=False, dry_run_limit=10):
    fs = list_wikidata_parts_file(dump_folder)
    if dry_run:
        counter = 0
        ret = []
        for f in tqdm(fs):
            for item in iter_jsonl(f):
                counter += 1
                if counter >= dry_run_limit:
                    return ret
                ret.append(process_entity(item))
        return ret
    else:
        batch_results = []
        with tqdm(desc="Processing items", unit=" item ", mininterval=0.5) as pbar:
            for f in fs:
                pbar.set_description(f"Processing file: {f}")
                for item in iter_jsonl(f):
                    pbar.update(1)
                    entity_id = item['id']
                    not_p = not entity_id.startswith('P')

                    process_labels = True
                    process_desc = True
                    process_aliases = True
                    process_claims = True

                    if not_p and not has_english_wikipedia_link(item):
                        process_labels = has_english_label(item)
                        process_desc = False
                        process_aliases = False
                        process_claims = False

                    batch_results.append(
                        process_entity(
                            item,
                            process_labels=process_labels,
                            process_desc=process_desc,
                            process_aliases=process_aliases,
                            process_claims=process_claims
                        )
                    )
                    if len(batch_results) == batch_size:
                        with db_proxy.atomic():
                            insert_wikidata_batch(batch_results, batch_size)
                            batch_results.clear()

        if len(batch_results) > 0:
            # TODO: insert everything into database
            with db_proxy.atomic():
                insert_wikidata_batch(batch_results, batch_size)
            batch_results.clear()


def list_wikidata_parts_file(dump_folder):
    fs = listdir(dump_folder)
    fs = [f for f in fs if f.endswith('.jsonl') or f.endswith('.jsonl.bz2')]
    return sorted(fs)


def init_wikidata():
    db_proxy.create_tables(
        [WikidataEntityLabel, WikidataEntityDescriptions, WikidataEntityAliases, WikidataClaim,
         WikidataEntityEnSiteLink])
