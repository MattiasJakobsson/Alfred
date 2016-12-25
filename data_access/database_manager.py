from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


class DatabaseManager:
    def __init__(self):
        self.db = TinyDB('~/db.json', storage=CachingMiddleware(JSONStorage))

    def insert(self, category, data):
        table = self.db.table(category)

        table.insert(data)
