import requests
from xml.etree import ElementTree


def get_available_settings():
    return ['ip_address']


def get_type():
    return VieraTv


class VieraTv:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager

    def _send_request(self, command):
        body = (
            "<?xml version='1.0' encoding='utf-8'?> \
               <s:Envelope xmlns:s='http://schemas.xmlsoap.org/soap/envelope/' \
               s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/'> \
                <s:Body> \
                 <u:X_SendKey xmlns:u='urn:panasonic-com:service:p00NetworkControl:1'> \
                  <X_KeyEvent>" + command + "</X_KeyEvent> \
                 </u:X_SendKey> \
                </s:Body> \
               </s:Envelope>"
        )

        headers = {
            'Content-Length': str(len(body)),
            'Content-Type': 'text/xml; charset="utf-8"',
            'SOAPACTION': '"urn:panasonic-com:service:p00NetworkControl:1#X_SendKey"'
        }

        ip = self.settings_manager.get_setting('ip_address')

        requests.post('http://%s:55000/nrc/control_0' % ip, data=body, headers=headers)

    def _get_response(self, query):
        body = (
            "<?xml version='1.0' encoding='utf-8'?> \
               <s:Envelope xmlns:s='http://schemas.xmlsoap.org/soap/envelope/' \
               s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/'> \
                <s:Body> \
                 <u:" + query + " xmlns:u='schemas-upnp-org:service:RenderingControl:1'> \
                  <InstanceID>0</InstanceID><Channel>Master</Channel> \
                 </u:" + query + "> \
                </s:Body> \
               </s:Envelope>"
        )

        headers = {
            'Content-Length': str(len(body)),
            'Content-Type': 'text/xml; charset="utf-8"',
            'SOAPACTION': '"urn:schemas-upnp-org:service:RenderingControl:1#%s"' % query
        }

        ip = self.settings_manager.get_setting('ip_address')

        return requests.post('http://%s:55000/dmr/control_0' % ip, data=body, headers=headers)

    def toggle_power(self):
        self._send_request('NRC_POWER-ONOFF')

    def switch_hdmi_input_to(self, hdmi):
        self._send_request('NRC_HDMI%s-ONOFF' % hdmi)

    def volume_up(self):
        self._send_request('NRC_VOLUP-ONOFF')

    def volume_down(self):
        self._send_request('NRC_VOLDOWN-ONOFF')

    def mute(self):
        self._send_request('NRC_MUTE-ONOFF')

    def get_volume(self):
        try:
            response = self._get_response('GetVolume')

            response.raise_for_status()

            root = ElementTree.fromstring(response.content)

            return root.find('.//CurrentVolume').text
        except:
            return ''

    def get_power_status(self):
        try:
            response = self._get_response('GetVolume')

            response.raise_for_status()

            return True
        except:
            return False
