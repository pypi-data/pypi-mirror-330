from functools import lru_cache
from .db import WikidataEntityEnSiteLink


def create_link(site_link_name: str, lang='en') -> str:
    title = site_link_name.replace(' ', '_')
    return f"https://{lang}.wikipedia.org/wiki/{title}"


@lru_cache(maxsize=1024 * 30)
def lookup_wikilink(entity, default_value=None):
    """
    lookup wikilink by entity id
    :param entity: wikidata entity id
    :return:
    """
    item = WikidataEntityEnSiteLink.get_or_none(
        WikidataEntityEnSiteLink.entity_id == entity,
    )
    if item:
        return create_link(item.title)
    else:
        return default_value
