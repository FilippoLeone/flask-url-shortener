from database import connector
from datetime import datetime
from utils import utils, logger
import sqlite3

class execute_query:
    def __init__(self):
        self.log = logger().log_error

    def get_url(self, identifier):
        try:
            connection = connector(permission='ro').connect()
            cursor = connection.cursor()
            cursor.execute("SELECT full_url FROM url_list WHERE shortlink=?", (identifier,))
            return cursor.fetchone()
        except (sqlite3.DatabaseError, sqlite3.ProgrammingError, sqlite3.OperationalError) as err:
            self.log(get_url=err)
            return False
        finally:
            connection.close()

    def get_all_records(self):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            for row in cursor.execute("SELECT * FROM url_list"):
                print(row)
        except (sqlite3.DatabaseError, sqlite3.ProgrammingError, sqlite3.OperationalError) as err:
            self.log(get_all_records=err)
        finally:
            connection.close()

    def store_record(self, full_url, *, expiration_date=None):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            shortlink = utils().generate_string()
            cursor.execute("""
            INSERT INTO url_list VALUES (NULL, ?, ?, ?, ?)
            """, [(full_url), (shortlink), (datetime.now().strftime("%Y-%m-%d %H:%M:%S")), (expiration_date)])
            connection.commit()
        except (sqlite3.DatabaseError, sqlite3.ProgrammingError, sqlite3.OperationalError) as err:
            self.log(store_record=err)
        finally:
            connection.close()
            return f'https://shortlinks.airhelp.com/{shortlink}'


    def add_api_key(self, owner, permission='ALL'):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            apikey = utils().generate_string(24)
            cursor.execute("""
            INSERT INTO api_keys VALUES (NULL, ?, ?, ?)
            """, [(owner), (apikey), (permission)])
            connection.commit()
            return apikey
        except (sqlite3.DatabaseError, sqlite3.ProgrammingError, sqlite3.OperationalError) as err:
            self.log(store_record=err)
        finally:
            connection.close()

    def check_api_key(self, key):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT key FROM api_keys WHERE key=?", (key,))
            ''.join(cursor.fetchone()) # Trying to join if execute above returns something
            return True
        except (sqlite3.DatabaseError, sqlite3.ProgrammingError, sqlite3.OperationalError, TypeError) as err:
            self.log(key_check=err)
            return False
        finally:
            connection.close()

    def get_table_struct(self):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT sql FROM sqlite_master")
            return ''.join(cursor.fetchone())
        except (sqlite3.DatabaseError, sqlite3.ProgrammingError, sqlite3.OperationalError, TypeError) as err:
            self.log(tablestruct=err)
        finally:
            connection.close()