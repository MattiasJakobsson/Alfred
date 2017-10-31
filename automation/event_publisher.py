import fnmatch
import logging
import uuid


subscriptions = []


def publish_event(event_name, event_data):
    subscribers = [item['callback'] for item in subscriptions if fnmatch.fnmatch(event_name, item['event_name'])]

    logging.info('Found %s subscribers for event %s' % (str(len(subscribers)), event_name))

    for subscriber in subscribers:
        subscriber(event_name, event_data)


def subscribe(event_name, callback):
    subscription_id = str(uuid.uuid4())

    subscriptions.append({'id': subscription_id, 'event_name': event_name, 'callback': callback})

    return {
        'dispose': lambda: un_subscribe(subscription_id)
    }


def un_subscribe(subscription_id):
    item = next(subscription for subscription in subscriptions if subscription['id'] == subscription_id)

    subscriptions.remove(item)
