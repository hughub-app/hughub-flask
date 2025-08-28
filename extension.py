# Store the database connection or ORM instance here
from flask import abort

class FakeQuery:
    def __init__(self, model, storage):
        self.model = model
        self.storage = storage

    def all(self):
        return list(self.storage.values())

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def get_or_404(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            abort(404, description=f"{self.model.__name__} with id {obj_id} not found")
        return obj


class FakeSession:
    def __init__(self, storage):
        self.storage = storage
        self.id_counter = 1

    def add(self, obj):
        obj.id = self.id_counter
        self.storage[self.id_counter] = obj
        self.id_counter += 1

    def delete(self, obj):
        if obj.id in self.storage:
            del self.storage[obj.id]

    def commit(self):

        pass


class FakeDB:
    def __init__(self):
        self._tables = {}     
        self.sessions = {}    

    def register_model(self, model):
        table_name = model.__name__

        if table_name not in self._tables:
            self._tables[table_name] = {}
            self.sessions[table_name] = FakeSession(self._tables[table_name])
            model.query = FakeQuery(model, self._tables[table_name])

    @property
    def session(self):

        return self.sessions.get('Child')


db = FakeDB()


