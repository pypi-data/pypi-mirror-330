from functools import lru_cache
from .db import WikidataEntityLabel


@lru_cache(maxsize=1024 + 30)  # Adjust size as needed
def lookup_label(entity, lang='en'):
    item = WikidataEntityLabel.get_or_none(
        WikidataEntityLabel.entity_id == entity,
        WikidataEntityLabel.language == lang,
    )
    return item.value if item else entity
