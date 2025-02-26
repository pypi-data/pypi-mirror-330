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
    print('Creating indexes for WikipediaArticle.')
    create_index(conn, 'WikipediaArticle', ['title', 'lang'])
    create_index(conn, 'WikipediaArticle', ['lang', 'title'])

    # Creating indexes for WikipediaArticleLinks
    print('Creating indexes for WikipediaArticleLinks.')
    create_index(conn, 'WikipediaArticleLinks', ['source_article', 'target_article_name'])
    create_index(conn, 'WikipediaArticleLinks', ['target_article_name', 'source_article'])

    print('Indexes created.')

    # Close the connection
    conn.close()
    print('Database connection closed.')
