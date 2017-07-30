from tinydb import TinyDB
import threading

lock = threading.RLock()


class DatabaseManager:
    def __init__(self):
        self.db = TinyDB('.data/db.json')

    def insert(self, category, data):
        with lock:
            table = self.db.table(category)

            return table.insert(data)

    def delete(self, category, eid):
        with lock:
            table = self.db.table(category)

            table.remove(eids=[eid])

    def update(self, category, eid, data):
        with lock:
            table = self.db.table(category)

            table.update(data, eids=[eid])

    def get_all(self, category):
        with lock:
            table = self.db.table(category)

            return table.all()

    def get_by_id(self, category, eid):
        with lock:
            table = self.db.table(category)

            return table.get(eid=eid)

    def get_by_condition(self, category, cond):
        with lock:
            table = self.db.table(category)

            return table.get(cond=cond)
