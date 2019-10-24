import sqlite3
from utils import logger

class connector:
    def __init__(self, *, permission='rw'):
        self.dbname = 'shortlinks.db'
        self.permission = permission
        self.log = logger().log_error

    def __enter__(self):
        self.conn = self.connect()
        return self.conn

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type or exception_value or traceback:
            self.log(exception_type=exception_value)
            return False
        self.conn.close()

    def connect(self):
        try:
            return sqlite3.connect(f"file:{self.dbname}?mode={self.permission}", uri=True)
        except sqlite3.OperationalError as e:
            self.log(sqlconnect=e)

    def create_db(self):
        try:
            sqlite3.connect(f"file:{self.dbname}?mode=rwc", uri=True)
        except sqlite3.OperationalError as e:
            self.log(drystart_error=e)
            return False