from plugins.plugin_base import PluginBase
import requests
import json
import base64


def get_available_settings():
    return ['ip', 'port', 'username', 'password']


def get_type():
    return Zway


class Zway(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager)

    def _get(self, path):
        info = ('%s:%s' % (self._get_setting('username'), self._get_setting('password'))).encode('utf-8')

        authorization = base64.b64encode(info).decode('utf-8')

        return json.loads(requests.get('http://%s:%s/ZAutomation/api%s' % (self._get_setting('ip'),
                                                                           self._get_setting('port'), path),
                                       headers={'Accept': 'application/json',
                                                'Authorization': 'Basic %s' % authorization}).text)

    def get_instances(self):
        data = self._get('/v1/instances')

        return data['data']

    def get_devices(self):
        data = self._get('/v1/devices')

        return data['data']['devices']

    def execute_device_command(self, device_id, command, parameters):
        path = '/v1/devices/%s/command/%s?%s' % (device_id, command, parameters)

        self._get(path)
