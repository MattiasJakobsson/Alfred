subscriptions = []


def publish_event(event_name, event_data):
    subscribers = [item['callback'] for item in subscriptions if item['event_name'] == event_name]

    for subscriber in subscribers:
        subscriber(event_data)


def subscribe(event_name, callback):
    subscriptions.append({'event_name': event_name, 'callback': callback})
