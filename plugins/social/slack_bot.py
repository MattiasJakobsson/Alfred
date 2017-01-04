import requests
import json
from plugins.plugin_base import PluginBase


def get_available_settings():
    return ['api_token']


def get_type():
    return SlackBot


class SlackBot(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager)

    def _post(self, endpoint, parameters):
        parameters['token'] = self._get_setting('api_token')

        response = requests.post('https://slack.com/api/%s' % endpoint, data=parameters)

        return json.loads(response.text)

    def send_message(self, channel, message):
        self._post('chat.postMessage', {'channel': channel, 'text': message})
