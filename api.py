from flask import Flask, request, render_template
from datetime import datetime

from acme import model, logic


app = Flask(__name__)


API_ROOT = '/api/v1'
EVENT_API_ROOT = API_ROOT + '/event'


my_storage = logic.Event_logic()


class API_exeption(Exception):
    pass


def from_raw_to_event(raw_event: str) -> model.Event:   #форматирование из строки (self, id: int, day: datetime, title: str, text: str):
    try:
        event_list_data = raw_event.split('|')
        event_id = event_list_data[0].replace('-', '')  #т.к. в ТЗ ограничение - одно событие в день, id формирую из даты события (уникален у каждого события)
        day = datetime.strptime(event_list_data[0], '%Y-%m-%d')
        title = event_list_data[1]
        text = event_list_data[2]
        event = model.Event(event_id, day, title, text)
        return event
    except Exception as ex:
        raise API_exeption('Некорректный формат ввода')


def to_raw(event: model.Event) -> str:
    return f'{event.day.strftime("%Y-%m-%d")}|{event.title}|{event.text}'


@app.route(EVENT_API_ROOT + '/', methods=['POST'])
def create():
    try:
        data = request.get_data().decode('utf-8')
        event = from_raw_to_event(data)     #  экземпляр класса Event
        my_storage.create(event)
        return f'New event created: {event.title}. Date: {event.day.strftime("%Y-%m-%d")}. id: {event.event_id}'
    except Exception as ex:
        return f'Failed: {ex}'

@app.route(EVENT_API_ROOT + '/', methods=['GET'])
def list():
    try:
        raw = ''
        for elem in my_storage.list():
            raw += to_raw(elem) + '\n'
        return raw
    except Exception as ex:
        return f'Failed: {ex}'



@app.route(EVENT_API_ROOT + '/<event_id>/', methods=['GET'])
def read(event_id: str):
    try:
        result = my_storage.read(event_id)
        return to_raw(result)
    except Exception as ex:
        return f'Failed: {ex}'


@app.route(EVENT_API_ROOT + '/<event_id>/', methods=['PUT'])
def update(event_id: str):
    try:
        data = request.get_data().decode('utf-8')
        event = from_raw_to_event(data)
        my_storage.update(event_id, event)
        return f'Event id: {event_id} updated'
    except Exception as ex:
        return f'Failed: {ex}'



@app.route(EVENT_API_ROOT + '/<event_id>/', methods=['DELETE'])
def delete(event_id: str):
    try:
        my_storage.delete(event_id)
        return f'Event id:{event_id} deleted'
    except Exception as ex:
        return f'Failed: {ex}'



if __name__ == '__main__':
    app.run(debug=True)