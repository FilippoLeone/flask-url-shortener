import sqlite3
from utils import logger

class connector:
    def __init__(self, *, permission='rw'):
        self.first_start = False
        self.dbname = 'shortlinks.db'
        self.permission = permission
        self.log = logger().log_error

    def create_db(self):
        sqlite3.connect(f"file:{self.dbname}?mode=rwc", uri=True)
        self.create_default_tables()

    def connect(self):
        try:
            return sqlite3.connect(f"file:{self.dbname}?mode={self.permission}", uri=True)
        except sqlite3.OperationalError as e:
            self.log(sqlconnect=e)

    def create_url_table(self):
        # Creating url table
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute("""
            CREATE TABLE url_list
            (id INTEGER PRIMARY KEY AUTOINCREMENT, full_url TEXT, shortlink TEXT UNIQUE, creation_date TEXT, expiration_date TEXT)
            """)
            connection.commit()
        except (sqlite3.DatabaseError, sqlite3.ProgrammingError, sqlite3.OperationalError) as err:
            self.log(url_table=err)
        finally:
            connection.close()

    def create_apikey_table(self):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            # Creating API key table
            cursor.execute("""
            CREATE TABLE api_keys
            (id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT UNIQUE, key TEXT UNIQUE, permissions TEXT)
            """)
            connection.commit()
        except (sqlite3.DatabaseError, sqlite3.ProgrammingError, sqlite3.OperationalError) as err:
            self.log(apikey_table=err)
        finally:
            connection.close()

    def create_default_tables(self):
        self.create_url_table()
        self.create_apikey_table()