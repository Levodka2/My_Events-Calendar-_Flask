from acme import storage
from acme import model

class DB_Exception(Exception):
    pass

class DB:
    def __init__(self):
        self.storage = storage.Local_Storage()


    def create(self, event: model.Event):
        try:
            self.storage.create(event)
        except Exception:
            return DB_Exception('Failed to create')


    def list(self):
        try:
            return self.storage.list()
        except Exception:
            return DB_Exception('Failed to list')


    def read(self, event_id: str):
        try:
            return self.storage.read(event_id)
        except Exception:
            return DB_Exception('Event not found')


    def update(self, event_id: str, event: model.Event):
        try:
            self.storage.update(event_id, event)
        except Exception:
            return DB_Exception('Failed to update')


    def delete(self, event_id: str):
        try:
            self.storage.delete(event_id)
        except Exception:
            return DB_Exception('Failed to delete')