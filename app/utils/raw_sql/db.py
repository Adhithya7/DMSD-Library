import psycopg2 as psql
import os
from dotenv import load_dotenv

def make_connection():
    conn_string = f"dbname='{os.environ.get('DB_NAME')}' port='{os.environ.get('DB_PORT')}' user='{os.environ.get('DB_USER')}' password='{os.environ.get('DB_PWD')}' host='{os.environ.get('DB_HOST')}' "
    connection = psql.connect(conn_string)
    psql_cursor = connection.cursor()
    return connection, psql_cursor

load_dotenv()
connection, cursor = make_connection()
