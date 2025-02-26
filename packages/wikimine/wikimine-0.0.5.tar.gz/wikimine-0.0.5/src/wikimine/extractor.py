from .db import WikidataClaim
from .labels import lookup_label


class Aggregator(object):

    @staticmethod
    def first_or_none(vs):
        if len(vs) == 0:
            return None
        return vs[0]

    @staticmethod
    def default_agg(x):
        return x

    @staticmethod
    def min(vs):
        if len(vs) == 0:
            return None
        return min(vs)

    @staticmethod
    def max(vs):
        if len(vs) == 0:
            return None
        return max(vs)


class ClaimExtractor(object):

    @staticmethod
    def get_target_label(t):
        return lookup_label(t.target_entity)

    @staticmethod
    def get_target_label_and_id(t):
        eid = t.target_entity
        label = lookup_label(eid)
        return {
            'id': eid,
            'label': label
        }

    @staticmethod
    def get_target_value(claim):
        return claim.body

    @staticmethod
    def get_target_text_value(claim):
        return (
            claim.body
            .get('mainsnak', {})
            .get('datavalue', {})
            .get('value', {})
            .get('text')
        )

    @staticmethod
    def get_target_value_year(claim):
        time_value = (
            claim.body
            .get('mainsnak', {})
            .get('datavalue', {})
            .get('value', {})
            .get('time')
        )

        if time_value:
            return int(time_value[:5])
        return None


def gather(source_entity, prop_id, map_fn, agg_fn):
    claim = WikidataClaim.select().where(
        WikidataClaim.source_entity == source_entity,
        WikidataClaim.property_id == prop_id,
    )

    if map_fn is None:
        map_fn = ClaimExtractor.get_target_label

    if agg_fn is None:
        agg_fn = Aggregator.default_agg

    return agg_fn([map_fn(c) for c in claim])


def fetch(name, prop_id, map_fn=None, agg_fn=None):
    return (name, prop_id, map_fn, agg_fn)


def gather_all(
        source_entity,
        cfg,
        name_field='name',
        entity_id_field='entity_id',
):
    item = {}
    for (name, prop_id, map_fn, agg_fn) in cfg:
        item[name] = gather(source_entity, prop_id, map_fn, agg_fn)

    item[name_field] = lookup_label(source_entity)
    item[entity_id_field] = source_entity
    return item
