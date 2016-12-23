import requests
import xml.etree.ElementTree as ET
from components.routers.tilgin.router_api import RouterApi


class AmplifierApi:
    def __init__(self):
        self.router_api = RouterApi()

    def find_amp(self, mac_address):
        devices = self.router_api.get_connected_devices()

        items = [item for item in devices if 'mac' in item and item['mac'] == mac_address]

        ip = items[0]['ip']

        return Marantz(ip)


class Marantz:
    def __init__(self, ip):
        self.ip = ip

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

        print(status)

        if status['power']:
            self._send_command('PutZone_OnOff/OFF')
        else:
            self._send_command('PutZone_OnOff/ON')
