import requests
from components.routers.tilgin.router_api import RouterApi


class TvApi:
    def __init__(self):
        self.router_api = RouterApi()

    def find_tv(self, mac_address):
        devices = self.router_api.get_connected_devices()

        items = [item for item in devices if 'mac' in item and item['mac'] == mac_address]

        ip = items[0]['ip']

        return Viera(ip)


class Viera:
    def __init__(self, ip):
        self.ip = ip

    def _send_request(self, command):
        body = (
            "<?xml version='1.0' encoding='utf-8'?> \
               <s:Envelope xmlns:s='http://schemas.xmlsoap.org/soap/envelope/' \
               s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/'> \
                <s:Body> \
                 <u:X_SendKey xmlns:u='urn:panasonic-com:service:p00NetworkControl:1'> \
                  " + command + " \
                 </u:X_SendKey> \
                </s:Body> \
               </s:Envelope>"
        )

        headers = {
            'Content-Length': str(len(body)),
            'Content-Type': 'text/xml; charset="utf-8"',
            'SOAPACTION': '"urn:panasonic-com:service:p00NetworkControl:1#X_SendKey"'
        }

        requests.post('http://%s:55000/nrc/control_0' % self.ip, data=body, headers=headers)

    def power(self):
        self._send_request('<X_KeyEvent>NRC_POWER-ONOFF</X_KeyEvent>')
