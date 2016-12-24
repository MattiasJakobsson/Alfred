import requests
from xml.etree import ElementTree


def get_available_settings():
    return ['ip_address']


def get_type():
    return MarantzAmp


class MarantzAmp:
    def __init__(self, plugin_id, settings_manager):
        self.plugin_id = plugin_id
        self.settings_manager = settings_manager

    def _send_command(self, command):
        body = 'cmd0=%s' % command

        headers = {
            'Content-Type': 'text/html'
        }

        requests.post('http://%s/MainZone/index.put.asp' %
                      self.settings_manager.get_setting(self.plugin_id, 'ip_address'), data=body, headers=headers)

    def _get_status(self):
        response = requests.get('http://%s/goform/formMainZone_MainZoneXml.xml' %
                                self.settings_manager.get_setting(self.plugin_id, 'ip_address'))

        root = ElementTree.fromstring(response.content)

        power = root.find('Power').find('value').text == 'ON'

        return {'power': power}

    def toggle_power(self):
        status = self._get_status()

        if status['power']:
            self._send_command('PutZone_OnOff/OFF')
        else:
            self._send_command('PutZone_OnOff/ON')
