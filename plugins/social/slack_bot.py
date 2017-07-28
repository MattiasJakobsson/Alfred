from plugins.plugin_base import PluginBase
from slackclient import SlackClient
from threading import Thread
import time
import uuid
import logging


message_receivers = {}


def get_available_settings():
    return ['api_token']


def get_type():
    return SlackBot


class SlackMessageReceiverThread(Thread):
    def __init__(self, client, message_arrived):
        super(SlackMessageReceiverThread, self).__init__()

        self._client = client
        self._running = True
        self._message_arrived = message_arrived

    def start(self):
        self._client.rtm_connect()

        while self._running:
            new_messages = [m for m in self._client.rtm_read() if m['type'] == 'message']
            print(new_messages)
            for message in new_messages:
                self._message_arrived('slack_message_received', {
                    'message': message['text'],
                    'from': message['user']
                })

            time.sleep(1)

    def stop(self):
        self._running = False


class SlackBot(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager)
        self._slack_client = None

    def send_message(self, channel, message):
        client = self._get_client()

        client.api_call('chat.postMessage',
                        channel='#%s' % channel,
                        text=message,
                        parse='full')

    def start_receiving_messages(self):
        client = self._get_client()

        thread = SlackMessageReceiverThread(client, self._apply)

        message_receivers[self._plugin_id] = thread

    def stop_receiving_messages(self):
        if self._plugin_id in message_receivers:
            logging.info('Shutting down slack bot background thread')
            message_receivers[self._plugin_id].stop()

            del message_receivers[self._plugin_id]

    def get_automations(self):
        self.start_receiving_messages()

        return [{
            'definition': {'initial_step': {
                'id': str(uuid.uuid4()),
                'type': '.workflows.steps.execute_plugin_command',
                'plugin_id': self._plugin_id,
                'command': 'start_receiving_messages',
                'parameters': {}
            }},
            'triggers': [{'type': '.workflows.triggers.event_listener_trigger', 'subscribe_to': 'workflows_started'}]
        }, {
            'definition': {'initial_step': {
                'id': str(uuid.uuid4()),
                'type': '.workflows.steps.execute_plugin_command',
                'plugin_id': self._plugin_id,
                'command': 'stop_receiving_messages',
                'parameters': {}
            }},
            'triggers': [{'type': '.workflows.triggers.event_listener_trigger', 'subscribe_to': 'workflows_stopped'}]
        }]

    def _get_client(self):
        if self._slack_client is not None:
            return self._slack_client

        self._slack_client = SlackClient(self._get_setting('api_token'))

        return self._slack_client
