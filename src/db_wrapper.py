import sqlite3
import os
from uuid import uuid4
from datetime import datetime, timezone

SCHEMA_SCRIPT = """CREATE TABLE reports (
      id TEXT PRIMARY KEY,
      path TEXT,
      name TEXT,
      submitted_date DATETIME
    );
    """

class Model(object):
    db = None
    db_connection = None

    @classmethod
    def init_db(cls, db_file_path):
        if not os.path.exists(db_file_path):
            cls._create_db(db_file_path)
        cls.db = db_file_path
        cls.db_connection = sqlite3.connect(db_file_path)

    @classmethod
    def _create_db(cls, db_file_path):
        connection = sqlite3.connect(db_file_path)
        cursor = connection.cursor()
        cursor.executescript(SCHEMA_SCRIPT)
        connection.commit()
        cursor.close()
        cls.db = db_file_path
        cls.db_connection = connection


class Entry(Model):
    """
    Wrapper around sqlite3 DB
    """
    def __init__(self, entry_id=None):
        self.entry_id = entry_id or str(uuid4())
        super().__init__()

    def save(self):
        """
        To be implemented by child classes
        """
        raise NotImplementedError

    def update(self):
        """
        To be implemented by child classes
        """
        raise NotImplementedError

    def validate(self):
        """
        To be implemented by child classes
        """
        raise NotImplementedError

    def find_by_id(self, entry_id):
        """
        To be implemented by child classes
        """
        raise NotImplementedError


class Report(Entry):
    """
    Implements an Report record
    """
    table = 'reports'

    def __init__(self, path, name, submitted_date=None):
        self.path = path
        self.name = name
        self.submitted_date = submitted_date or datetime.now(tz=timezone.utc).timestamp()
        super().__init__()

    def validate(self):
        pass

    def update(self):
        pass

    def save(self):
        self.validate()
        insert_template = 'INSERT INTO reports(id, path, name, submitted_date) VALUES (?,?,?,?)'

        try:
            cur = self.db_connection.cursor()
            cur.execute(insert_template, (self.entry_id, self.path, self.name, self.submitted_date))
        except sqlite3.DatabaseError:
            raise # Log the error here
        finally:
            cur.close()
        self.db_connection.commit()

    def find_by_id(self, entry_id):
        query = f'SELECT * FROM {self.table} WHERE id IS {entry_id}'
        cur = self.db_connection.cursor()
        try:
            return cur.execute(query).fetchone()
        except sqlite3.DatabaseError:
            raise # Log the error here
        finally:
            cur.close()

    @classmethod
    def find_all(cls):
        cur = cls.db_connection.cursor()
        cur.execute(f'SELECE * FROM {cls.table}')
        try:
            while True:
                enrties = cur.fetchmany(20)
                for entry in enrties:
                    yield entry
                if not enrties:
                    break
        except sqlite3.DatabaseError:
            raise # Log the error here
        finally:
            cur.close()
