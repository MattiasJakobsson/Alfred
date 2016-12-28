import json
import requests
from collections import namedtuple

"https://github.com/cjlarose/pyeventstore/tree/master/pyeventstore"

Event = namedtuple('Event', ['id', 'type', 'data'])


def publish_events(head_uri, events):
    def event_to_json(event):
        return {
            'eventId': str(event.id),
            'eventType': event.type,
            'data': event.data
        }

    headers = {'Content-Type': 'application/vnd.eventstore.events+json'}
    payload = json.dumps([event_to_json(e) for e in events])
    response = requests.post(head_uri, headers=headers, data=payload)

    if 400 <= response.status_code < 500:
        raise ValueError(response.reason)


class Client:
    def __init__(self, host, secure=False, port=2113):
        proto = "https" if secure else "http"
        self.uri_base = '{}://{}:{}'.format(proto, host, port)

    def publish_events(self, stream_name, events):
        uri = self._stream_head_uri(stream_name)

        return publish_events(uri, events)

    def _stream_head_uri(self, stream_name):
        return '{}/streams/{}'.format(self.uri_base, stream_name)
