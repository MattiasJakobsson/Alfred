import fnmatch
import logging


subscriptions = []


def publish_event(event_name, event_data):
    subscribers = [item['callback'] for item in subscriptions if fnmatch.fnmatch(event_name, item['event_name'])]

    logging.info('Found %s subscribers for event %s' % (str(len(subscribers)), event_name))

    for subscriber in subscribers:
        subscriber(event_data)


def subscribe(event_name, callback):
    subscriptions.append({'event_name': event_name, 'callback': callback})
