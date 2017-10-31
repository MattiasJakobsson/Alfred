import json
import collections
from automation.event_publisher import subscribe


event_list = collections.deque(maxlen=30)


def log_event(event_name, event_data):
    event_list.append({'event_name': event_name, 'event_data': event_data})

subscribe('*', log_event)


def bootstrap(application):
    log = Log()

    application.add_route('/log', log)


class Log:
    def on_get(self, req, resp):
        resp.body = '%s(%s)' % (req.params['jsoncallback'], json.dumps(list(reversed(event_list))))
