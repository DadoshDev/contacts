from typing import Union
import psycopg2
from psycopg2.extras import DictCursor, DictRow
from config.Config import DB_CONFIG


class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()

        if self.conn is not None:
            self.conn.close()

        if self.cursor is not None:
            self.cursor.close()

    def execute(self, query, params=None):
        """Execute queries (UPDATE, DELETE, INSERT)"""
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetchone(self, query, params=None):
        """Get one row from table"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query, params=None):
        """Get multiple rows from table"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


def execute_query(query, params=None, fetch=None) -> Union[DictRow, None, list]:
    try:
        with DatabaseManager() as db:
            if fetch == "one":
                return db.fetchone(query, params)
            elif fetch == "all":
                return db.fetchall(query, params)
            else:
                db.execute(query, params)
    except Exception as exc:
        print(exc)
        return None
