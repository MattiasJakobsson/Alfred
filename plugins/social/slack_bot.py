from plugins.plugin_base import PluginBase
from slackclient import SlackClient
import time
import uuid


def get_available_settings():
    return ['api_token']


def get_type():
    return SlackBot


class SlackMessageReceiver:
    def __init__(self, api_token):
        self._api_token = api_token
        self._running = False

    def start(self, trigger):
        slack_client = SlackClient(self._api_token)

        slack_client.rtm_connect()

        self._running = True

        while self._running:
            new_messages = [m for m in slack_client.rtm_read() if m['type'] == 'message' and 'user' in m]

            for message in new_messages:
                trigger(message)

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
                        channel=channel,
                        text=message,
                        parse='full')

    def receive_new_message(self, text, user, channel):
        self._apply('slack_message_received', {
            'message': text,
            'from': user,
            'channel': channel
        })

    def get_automations(self):
        return [{
            'definition': {'initial_step': {
                'id': str(uuid.uuid4()),
                'type': '.workflows.steps.execute_plugin_command',
                'plugin_id': self._plugin_id,
                'command': 'receive_new_message',
                'parameters': {
                    'text': '[??state["initial_state"]["text"] if "text" in state["initial_state"] else ""??]',
                    'user': '[??state["initial_state"]["user"] if "user" in state["initial_state"] else ""??]',
                    'channel': '[??state["initial_state"]["channel"] if "channel" in state["initial_state"] else ""??]'
                }
            }},
            'triggers': [{'type': '.workflows.triggers.background_task_trigger',
                          'task': 'plugins.social.slack_bot.SlackMessageReceiver',
                          'parameters': {
                              'api_token': self._get_setting('api_token')
                          }}]
        }]

    def _get_client(self):
        if self._slack_client is not None:
            return self._slack_client

        self._slack_client = SlackClient(self._get_setting('api_token'))

        return self._slack_client
