from database import connector
from datetime import datetime
from utils import utils

class execute_query:
    def get_url(self, identifier):
        try:
            connection = connector(permission='r').connect()
            cursor = connection.cursor()
            cursor.execute("SELECT full_url FROM url_list WHERE shortlink=?", (identifier,))
            return cursor.fetchone()
        except (ValueError):
            print('error')
            return False
        finally:
            connection.close()

    def get_all_records(self):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            for row in cursor.execute("SELECT * FROM url_list"):
                print(row)
        except:
            pass
        finally:
            connection.close()

    def store_record(self, full_url, *, expiration_date=None):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            shortlink = utils().generate_string()
            #print(f"I've created an alias on: {shortlink}")
            cursor.execute("""
            INSERT INTO url_list VALUES (NULL, ?, ?, ?, ?)
            """, [(full_url), (shortlink), (datetime.now().strftime("%Y-%m-%d %H:%M:%S")), (expiration_date)])
            connection.commit()
        except (KeyError, ValueError):
            print('error')
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
        except:
            pass
        finally:
            connection.close()

    def check_api_key(self, key):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT key FROM api_keys WHERE key=?", (key,))
            ''.join(cursor.fetchone()) # Trying to join if execute above returns something
            return True
        except TypeError:
            return False
        finally:
            connection.close()

    def get_table_struct(self):
        try:
            connection = connector().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT sql FROM sqlite_master")
            return ''.join(cursor.fetchone())
        except:
            pass
        finally:
            connection.close()