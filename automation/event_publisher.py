from data_access.event_store_manager import Client, Event
from uuid import uuid4


client = Client('localhost')
subscriptions = []


def publish_event(source, event_name, event_data):
    client.publish_events(source, [Event(uuid4(), event_name, event_data)])

    subscribers = [item['callback'] for item in subscriptions if item['event_name'] == event_name]

    for subscriber in subscribers:
        subscriber(event_data)


def subscribe(event_name, callback):
    subscriptions.append({'event_name': event_name, 'callback': callback})
