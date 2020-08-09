import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    if os.getenv('ENVIRONMENT') == 'LOCAL':
        conn = psycopg2.connect(os.getenv('POSTGRES_CONN_DETAIL'))
    else:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    return conn, cursor


def save_search(query):
    conn, cursor = get_db_connection()
    cursor.execute("""INSERT INTO search_query (q_str, q_tsv) VALUES ('{}', to_tsvector('{}'))""".format(query, query))
    conn.commit()
    print('query saved successfully!')
    conn.close()


def get_recent(query):
    conn, cursor = get_db_connection()
    cursor.execute("""SELECT q_str FROM search_query WHERE q_tsv @@ (plainto_tsquery('{}')) = true""".format(query))
    rows = cursor.fetchall()
    print('got recent queries successfully!')
    conn.close()
    if not rows:
        return 'No recent searches found for it.'
    return '\n'.join([r[0] for r in rows])
