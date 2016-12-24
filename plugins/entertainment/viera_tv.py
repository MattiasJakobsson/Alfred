import requests


def get_available_settings():
    return ['ip_address']


def get_type():
    return VieraTv


class VieraTv:
    def __init__(self, plugin_id, settings_manager):
        self.plugin_id = plugin_id
        self.settings_manager = settings_manager

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

        ip = self.settings_manager.get_setting(self.plugin_id, 'ip_address')

        requests.post('http://%s:55000/nrc/control_0' % ip, data=body, headers=headers)

    def toggle_power(self):
        self._send_request('<X_KeyEvent>NRC_POWER-ONOFF</X_KeyEvent>')
