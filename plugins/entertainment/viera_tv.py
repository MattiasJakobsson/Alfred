import requests


def get_name():
    return 'Viera TV'


def get_default_settings():
    return {'ip_address': ''}


def get_available_commands():
    return {'power': {}}


def get_available_queries():
    return {}


def create(settings):
    return VieraTv(settings)


class VieraTv:
    def __init__(self, settings):
        self.ip = settings['ip_address']

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
