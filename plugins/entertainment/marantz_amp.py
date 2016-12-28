import requests
from xml.etree import ElementTree


def get_available_settings():
    return ['ip_address']


def get_type():
    return MarantzAmp


class MarantzAmp:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager

    def _send_command(self, command):
        body = 'cmd0=%s' % command

        headers = {
            'Content-Type': 'text/html'
        }

        requests.post('http://%s/MainZone/index.put.asp' %
                      self.settings_manager.get_setting('ip_address'), data=body, headers=headers)

    def _get_status(self):
        response = requests.get('http://%s/goform/formMainZone_MainZoneXml.xml' %
                                self.settings_manager.get_setting('ip_address'))

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
