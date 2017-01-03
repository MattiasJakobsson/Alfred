from data_access.event_store_manager import Client, Event
from uuid import uuid4


client = Client('localhost')
events = {}


def publish_event(source, event_name, event_data):
    client.publish_events(source, [Event(uuid4(), event_name, event_data)])

    if source not in events:
        events[source] = []

    events[source].append({'name': event_name, 'data': event_data})


def subscribe(source, event_name, callback):
    a = 0


def get_events_for(eid):
    stream_id = 'plugins-%s' % str(eid)

    return events[stream_id] if stream_id in events else []
