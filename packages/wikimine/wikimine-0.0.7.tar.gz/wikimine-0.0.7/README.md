# wikimine

[![PyPI - Version](https://img.shields.io/pypi/v/wikimine.svg)](https://pypi.org/project/wikimine)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wikimine.svg)](https://pypi.org/project/wikimine)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install wikimine
```

## Motivation

`wikidata` contains a vast amount of knowledge structured as a graph.

Its data model enables a wide range of applications, allowing relationships
between entities to be stored and queried in a highly flexible way.

However, this flexibility comes with a steep learning curve for most
programmers.

To effectively use `wikidata`, a developer must understand its unique
structure, along with `triplestore/graph` databases and the `SPARQL` query
language—both of which currently have limited learning resources.

This project translates `wikidata` into a more familiar data modeling format
and uses only `SQLite`, eliminating the need to set up a specialized database
system.

As a tradeoff, our approach sacrifices some of `wikidata`'s original
flexibility and expressiveness, which make it so powerful for large-scale
knowledge representation.

However, it makes the data more accessible to developers while retaining much
of its usefulness.

With this, developers can explore `wikidata` using familiar tools and
workflows.

We hope `wikimine` serves as a gateway to `wikidata`, graph databases, and
the semantic web, encouraging more people to contribute to these ecosystems.

## Data Modeling

`wikimine` contains the following tables (using peewee ORM):

```python

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

```

## Usage

### Process the wikidata json dump

After download the dump

```shell
# first split the dump into smaller pieces for easier processing.
python -m wikimine.cli split ./path-to-dump ./path-to-workspace-folder
# parse and import to sqlite.
python -m wikimine.cli import /path/to/db ./path-to-workspace-folder
# build indices.
python -m wikimine.cli index /path/to/db
```

### Connect to db

```python
from wikimine import auto_connect, connect

"""
    Search for database path from the following source and connect to it automatically.
    1.  from environment variable [WIKIMINE_WIKIDATA_DB].
    2.  ~/.wikimine.config.json: {"db_path": "/path/to/db"}
"""
auto_connect()
# or
connect('/path/to/db')
```

### Label and Link lookup

```python
from wikimine import lookup_label, lookup_wikilink
import wikimine.relations as rel
import wikimine.entity as ent

print(ent.People.Descartes)
print(lookup_label(ent.People.Descartes))
print(lookup_wikilink(ent.People.Descartes))

print(lookup_label(rel.People.lang_written))
```

#### Other commonly used entity and relations

```python
from wikimine.utils import list_static_class_members
import wikimine.relations as rel
import wikimine.entity as ent

print('class People:')
for k, v in list_static_class_members(ent.People):
    print(f'  {k}: {v}')
print()

print('class Location:')
for k, v in list_static_class_members(ent.Location):
    print(f'  {k}: {v}')
print()

print('class Company:')
for k, v in list_static_class_members(ent.Company):
    print(f'  {k}: {v}')
print()

print('class WrittenWorks:')
for k, v in list_static_class_members(ent.WrittenWork):
    print(f'  {k}: {v}')
print()

```

### Query the knowledge graph

```python
from wikimine.query import

list_instances_of,
get_common_classes,
get_common_edges,
get_classes_of_instance,
get_profile,
get_tree

import wikimine.relations as rel
import wikimine.entity as ent
import pprint

# list first 50 people
print("List first 50 people")
people = list_instances_of(ent.CommonTypes.Human, limit=50)
pprint.pp(people)
print('\n ----- \n')

# get common type of instances
print("Get common type of instances")
common_classes = get_common_classes([
    ent.Company.VW,
    ent.Company.Xerox,
    ent.Company.Apple,
])
common_classes.print_summary()
print('\n ----- \n')

print('List commonly existed outgoing relations of a group of entity')
common_edges = get_common_edges(people)
common_edges.print_summary()
print('\n ----- \n')

print('List all classes of a given entity')
classes = get_classes_of_instance(ent.Company.Apple)
pprint.pp(classes)
print('\n ----- \n')

print('Get all outgoing edge and its value of a given entity')
profile = get_profile(ent.WrittenWork.A_Mathematical_Theory_of_Communication)
pprint.pp(profile)
print('\n ----- \n')

print('Show all types that are has human as a subtype recursively')
tree = get_tree(ent.CommonTypes.Human, rel.TypingRelations.subclass_of)
tree.show()
print('\n ----- \n')

print('Show all types that are sub types of human recursively')
tree = get_tree(ent.CommonTypes.Human, rel.TypingRelations.subclass_of, direction='backward')
tree.show()

```

## License

`wikimine` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
