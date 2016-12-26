from tinydb import TinyDB


class DatabaseManager:
    def __init__(self):
        self.db = TinyDB('c:/temp/db.json')

    def insert(self, category, data):
        table = self.db.table(category)

        return table.insert(data)

    def get_all(self, category):
        table = self.db.table(category)

        return table.all()

    def get_by_id(self, category, eid):
        table = self.db.table(category)

        return table.get(eid=eid)
