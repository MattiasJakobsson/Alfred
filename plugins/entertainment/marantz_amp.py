import requests
from xml.etree import ElementTree
from plugins.plugin_base import PluginBase
import uuid


def get_available_settings():
    return ['ip_address']


def get_type():
    return MarantzAmp


class MarantzAmp(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager,
                         default_state={'current_states': {'muted': False, 'power': False}})

    def _send_command(self, command):
        body = 'cmd0=%s' % command

        headers = {
            'Content-Type': 'text/html'
        }

        requests.post('http://%s/MainZone/index.put.asp' %
                      self._get_setting('ip_address'), data=body, headers=headers)

    def _get_status(self):
        response = requests.get('http://%s/goform/formMainZone_MainZoneXml.xml' %
                                self._get_setting('ip_address'))

        root = ElementTree.fromstring(response.content)

        power = root.find('Power').find('value').text == 'ON'
        muted = root.find('Mute').find('value').text == 'ON'

        return {'power': power, 'muted': muted}

    def toggle_power(self):
        status = self._get_status()

        if status['power']:
            self._send_command('PutZone_OnOff/OFF')
        else:
            self._send_command('PutZone_OnOff/ON')

    def power_on(self):
        self._send_command('PutZone_OnOff/ON')

    def power_off(self):
        self._send_command('PutZone_OnOff/OFF')

    def toggle_muted(self):
        status = self._get_status()

        if status['muted']:
            self._send_command('PutVolumeMute/OFF')
        else:
            self._send_command('PutVolumeMute/ON')

    def muted_on(self):
        self._send_command('PutVolumeMute/ON')

    def muted_off(self):
        self._send_command('PutVolumeMute/OFF')

    def get_power_status(self):
        status = self._get_status()

        return status['power']

    def get_muted_status(self):
        status = self._get_status()

        return status['muted']

    def update_state(self):
        active_states = self._get_status()

        if active_states['power'] != self._state['current_states']['power']:
            if active_states['power']:
                self._apply('amplifier_turned_on', {})
            else:
                self._apply('amplifier_turned_off', {})

        if active_states['muted'] != self._state['current_states']['muted']:
            if active_states['muted']:
                self._apply('amplifier_muted', {})
            else:
                self._apply('amplifier_un_muted', {})

    def get_automations(self):
        return [{
            'definition': {'initial_step': {
                'id': str(uuid.uuid4()),
                'type': '.workflows.steps.execute_plugin_command',
                'plugin_id': self._plugin_id,
                'command': 'update_state',
                'parameters': {}
            }},
            'triggers': [{'type': '.workflows.triggers.interval_trigger', 'interval': 10}]
        }]

    def _on_amplifier_turned_on(self, event_data):
        self._state['current_states']['power'] = True

    def _on_amplifier_turned_off(self, event_data):
        self._state['current_states']['power'] = False

    def _on_amplifier_muted(self, event_data):
        self._state['current_states']['muted'] = True

    def _on_amplifier_un_muted(self, event_data):
        self._state['current_states']['muted'] = False
