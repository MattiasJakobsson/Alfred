import requests
import xml.etree.ElementTree as ET


def get_name():
    return 'Marantz amplifier'


def get_default_settings():
    return {'ip_address': ''}


def get_available_commands():
    return {'power': {}}


def get_available_queries():
    return {}


def create(settings):
    return MarantzAmp(settings)


class MarantzAmp:
    def __init__(self, settings):
        self.ip = settings['ip_address']

    def _send_command(self, command):
        body = 'cmd0=%s' % command

        headers = {
            'Content-Type': 'text/html'
        }

        requests.post('http://%s/MainZone/index.put.asp' % self.ip, data=body, headers=headers)

    def _get_status(self):
        response = requests.get('http://%s/goform/formMainZone_MainZoneXml.xml' % self.ip)

        root = ET.fromstring(response.content)

        power = root.find('Power').find('value').text == 'ON'

        return {'power': power}

    def power(self):
        status = self._get_status()

        if status['power']:
            self._send_command('PutZone_OnOff/OFF')
        else:
            self._send_command('PutZone_OnOff/ON')
