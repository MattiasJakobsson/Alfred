from data_access.event_store_manager import Client, Event
from uuid import uuid4


client = Client('localhost')


def publish_event(source, event_name, event_data):
    client.publish_events(source, [Event(uuid4(), event_name, event_data)])
