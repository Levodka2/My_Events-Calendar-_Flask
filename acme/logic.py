from acme import db
from acme import model

TITLE_LIMIT = 30
TEXT_LIMIT = 200



class Logic_Exception(Exception):
    pass


class Event_logic:
    def __init__(self):
        self.db = db.DB()


    def check_logic_create(self, event: model.Event):
        if len(event.title) > TITLE_LIMIT:
            raise Logic_Exception(f'Title length > max: {TITLE_LIMIT}')
        elif len(event.text) > TEXT_LIMIT:
            raise Logic_Exception(f'Text length > max: {TEXT_LIMIT}')
        elif event.event_id in self.db.storage.storage.keys():
            raise Logic_Exception(f'You can not add more than one event for one day')

    def check_logic_update(self, event: model.Event):
        if len(event.title) > TITLE_LIMIT:
            raise Logic_Exception(f'Title length > max: {TITLE_LIMIT}')
        elif len(event.text) > TEXT_LIMIT:
            raise Logic_Exception(f'Text length > max: {TEXT_LIMIT}')

    def create(self, event: model.Event):
        self.check_logic_create(event)
        try:
            self.db.create(event)
        except Exception as ex:
            return f'Failed: {ex}'


    def list(self):
        try:
            return self.db.list()
        except Exception as ex:
            return Logic_Exception(f'Failed: {ex}')


    def read(self, event_id: str):
        try:
            return self.db.read(event_id)
        except Exception as ex:
            return Logic_Exception(f'Failed: {ex}')


    def update(self, event_id: str, event: model.Event):
        self.check_logic_update(event)
        try:
            self.db.update(event_id, event)
        except Exception as ex:
            return f'Failed: {ex}'


    def delete(self, event_id: str):
        try:
            self.db.delete(event_id)
        except Exception as ex:
            return Logic_Exception(f'Failed: {ex}')