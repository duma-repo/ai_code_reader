import json
import sqlite3
import hashlib


class SQLiteCache:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )
        self.conn.commit()

    def get(self, key):
        self.cursor.execute(
            """
            SELECT value FROM cache WHERE key = ?
            """,
            (key,),
        )
        row = self.cursor.fetchone()
        if row is None:
            return None
        return row[0]

    def set(self, key, value):
        
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)
            """,
            (key, value),
        )
        self.conn.commit()

class LLM_File_Cache:
    def __init__(self, cache):
        self.cache = cache
    
    def get(self, file, *key):
        with open(file, 'rb') as f:
            _md5 = hashlib.md5(f.read()).hexdigest()
        
        key = '_'.join([_md5, *key])
        text = self.cache.get(key)
        return json.loads(text) if text else None
    
    def set(self, file, *key, value):
        with open(file, 'rb') as f:
            _md5 = hashlib.md5(f.read()).hexdigest()

        key = '_'.join([_md5, *key])
        self.cache.set(key, json.dumps(value))


llm_file_cache = LLM_File_Cache(SQLiteCache('llm_file_cache.db'))