import sqlite3


def create_index(conn, table, columns, unique=False):
    unique_str = "UNIQUE" if unique else ""
    index_name = f"{'_'.join(columns)}_index"
    columns_str = ", ".join(columns)
    sql = f"CREATE {unique_str} INDEX IF NOT EXISTS {index_name} ON {table} ({columns_str})"
    conn.execute(sql)


def build_wikidata_index(db_path):
    conn = sqlite3.connect(db_path)
    print('Database connected.')
    print('wikidataentityensitelink entity_id')
    create_index(conn, 'wikidataentityensitelink', ['entity_id'])

    print('wikidataentitylabel entity_id language')
    create_index(conn, 'wikidataentitylabel', ['entity_id', 'language'])

    print('wikidataentitylabel language value')
    create_index(conn, 'wikidataentitylabel', ['language', 'value'])

    print('wikidataentitydescriptions entity_id language')
    create_index(conn, 'wikidataentitydescriptions', ['entity_id', 'language'])

    print('wikidataentityaliases entity_id language')
    create_index(conn, 'wikidataentityaliases', ['entity_id', 'language'])

    print('wikidataclaim source_entity property_id target_entity')
    create_index(conn, 'wikidataclaim', ['source_entity', 'property_id', 'target_entity'])

    print('wikidataclaim property_id target_entity')
    create_index(conn, 'wikidataclaim', ['property_id', 'target_entity'])

    print('wikidataclaim target_entity')
    create_index(conn, 'wikidataclaim', ['target_entity'])

    print('Indexes created.')

    # Close the connection
    conn.close()
    print('Database connection closed.')
