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
    entity_id = CharField()
    language = CharField()
    value = CharField()


class WikidataEntityDescriptions(BaseModel):
    entity_id = CharField()
    language = CharField()
    value = CharField()


class WikidataEntityAliases(BaseModel):
    entity_id = CharField()
    language = CharField()
    value = CharField()


class WikidataClaim(BaseModel):
    source_entity = CharField()
    property_id = CharField()
    body = JSONField()  # this is the
    target_entity = CharField(null=True)  # this is only true if mainsnak.datavalue is wikibase-entityid


def connect(path_to_db):
    database = SqliteExtDatabase(path_to_db, pragmas=(
        ('cache_size', -1024 * 64),  # 64MB page-cache.
        ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
        ('foreign_keys', 1)))  # Enforce foreign-key constraints.

    db_proxy.initialize(database)


def auto_connect():
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
