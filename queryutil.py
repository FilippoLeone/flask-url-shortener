from database import connector
from datetime import datetime
from utils import utils, logger
import sqlite3

class execute_query:
    def __init__(self):
        self.log = logger().log_error
        self.shortlinkURL = "https://shortlinks.airhelp.com"

    def get_url(self, identifier):
        with connector(permission='ro') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT full_url FROM url_list WHERE shortlink=?", (identifier,))
            return cursor.fetchone()

    def get_all_records(self):
        with connector() as conn:
            for row in conn.cursor().execute("SELECT * FROM url_list"):
                print(row)

    def store_record(self, full_url, *, expiration_date=None):
        with connector() as conn:
            shortlink = utils().generate_string()
            conn.cursor().execute("""
            INSERT INTO url_list VALUES (NULL, ?, ?, ?, ?)
            """, [(full_url), (shortlink), (datetime.now().strftime("%Y-%m-%d %H:%M:%S")), (expiration_date)])
            conn.commit()
            return f'{self.shortlinkURL}/{shortlink}'

    def add_api_key(self, owner, permission='ALL'):
        with connector() as conn:
            apikey = utils().generate_string(24)
            conn.cursor().execute("""
            INSERT INTO api_keys VALUES (NULL, ?, ?, ?)
            """, [(owner), (apikey), (permission)])
            conn.commit()
            return apikey

    def check_api_key(self, key):
        with connector() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key FROM api_keys WHERE key=?", (key,))
            ''.join(cursor.fetchone()) # Trying to join if execute above returns something
            return True

    def get_table_struct(self):
        with connector() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT sql FROM sqlite_master")
            return ''.join(cursor.fetchone())

    def create_url_table(self):
        # Creating url table
        with connector() as conn:
            conn.cursor().execute("""
            CREATE TABLE url_list
            (id INTEGER PRIMARY KEY AUTOINCREMENT, full_url TEXT, shortlink TEXT UNIQUE, creation_date TEXT, expiration_date TEXT)
            """)
            conn.commit()

    def create_apikey_table(self):
        with connector() as conn:
            # Creating API key table
            conn.cursor().execute("""
            CREATE TABLE api_keys
            (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT UNIQUE, key TEXT UNIQUE, permissions TEXT)
            """)
            conn.commit()

    def create_default_tables(self):
        connector().create_db()
        self.create_url_table()
        self.create_apikey_table()
