from functools import lru_cache
from .db import WikidataEntityEnSiteLink


def create_link(site_link_name: str, lang='en') -> str:
    title = site_link_name.replace(' ', '_')
    return f"https://{lang}.wikipedia.org/wiki/{title}"


@lru_cache(maxsize=1024 * 30)
def lookup_wikilink(entity):
    item = WikidataEntityEnSiteLink.get_or_none(
        WikidataEntityEnSiteLink.entity_id == entity,
    )
    return create_link(item.title) if item else entity
