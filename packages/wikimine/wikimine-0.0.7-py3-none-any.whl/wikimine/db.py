import json
import os

from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

# db = SqliteExtDatabase(':memory:')

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class WikidataEntityEnSiteLink(BaseModel):
    entity_id = CharField()
    title = CharField()


class WikidataEntityLabel(BaseModel):
    """
    wikidata entity label
    """
    entity_id = CharField()
    language = CharField()
    value = CharField()


class WikidataEntityDescriptions(BaseModel):
    """
    wikidata entity descriptions.
    example: (Q9191, 'en', 'René Descartes')
    """
    entity_id = CharField()
    language = CharField()
    value = CharField()


class WikidataEntityAliases(BaseModel):
    """
    wikidata entity aliases.
    example:
    (Q9191, 'en', 'Descartes')
    (Q9191, 'en', 'Cartesius')
    """
    entity_id = CharField()
    language = CharField()
    value = CharField()


class WikidataClaim(BaseModel):
    """
    wikidata claim contains Statements about wikidata items.
    (item, property, value).

    You can read more about this concept here:
    https://www.wikidata.org/wiki/Wikidata:Introduction

    This table is indexed by
        (source_entity, property_id, target_entity).
        (property_id, target_entity).
        (target_entity).
    """
    source_entity = CharField()  # entity id of item.
    property_id = CharField()
    body = JSONField()  # this is the claim body.
    target_entity = CharField(null=True)  # this is only true if mainsnak.datavalue is wikibase-entityid


def connect(path_to_db):
    database = SqliteExtDatabase(path_to_db, pragmas=(
        ('cache_size', -1024 * 64),  # 64MB page-cache.
        ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
        ('foreign_keys', 1)))  # Enforce foreign-key constraints.

    db_proxy.initialize(database)


def auto_connect():
    """
    Search for database path from the following source and connect to it automatically.
    1.  from environment variable [WIKIMINE_WIKIDATA_DB].
    2.  ~/.wikimine.config.json: {"db_path": "/path/to/db"}
    :return:
    """
    db_path = os.getenv('WIKIMINE_WIKIDATA_DB')
    if not db_path:
        cfg_file = os.path.expanduser('~/.wikimine.config.json')
        if os.path.exists(cfg_file):
            with open(cfg_file, 'r') as f:
                cfg = json.load(f)
                db_path = cfg['db_path']

    if db_path:
        connect(db_path)
    else:
        raise EnvironmentError('WIKIMINE_WIKIDATA_DB not set')
