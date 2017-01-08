import requests
from bs4 import BeautifulSoup

from data_access.cache_manager import cache
from plugins.plugin_base import PluginBase


def get_available_settings():
    return ['login_user', 'login_password']


def get_type():
    return TilginRouter


class TilginRouter(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager, default_state={'active_devices': [], 'all_devices': []})
        self.cache = cache.get_cache('tilgin_router', expire=300)

    def _get_api_cookies(self):
        login_user = self._get_setting('login_user')
        login_password = self._get_setting('login_password')

        payload = {'__formtok': '', '__user': login_user, '__auth': 'login',
                   '__pass': login_password}

        response = requests.post('http://192.168.1.1/', data=payload)

        return response.cookies

    def _sign_in(self):
        return self.cache.get(key='%s_cookies' % self._plugin_id, createfunc=self._get_api_cookies)

    def _get_active_devices(self):
        cookies = self._sign_in()

        response = requests.get('http://192.168.1.1/status/lan_clients/', cookies=cookies)

        soup = BeautifulSoup(response.text, 'lxml')

        clients_box = soup.find(id="content")

        result = []

        for table in clients_box.find_all('tbody'):
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                result.append({'name': columns[0].text, 'mac': columns[1].text, 'ip': columns[2].text,
                               'type': columns[3].text, 'media': columns[4].text})

        return result

    def get_active_devices(self):
        return self._state['active_devices']

    def get_ip_from_mac(self, mac_address):
        devices = self.get_active_devices()

        ips = [item['ip'] for item in devices if 'mac' in item and item['mac'] == mac_address]

        return ips[0] if len(ips) > 0 else ''

    def get_is_device_online(self, mac_address):
        devices = self.get_active_devices()

        return mac_address in [item['mac'] for item in devices]

    def update_state(self):
        active_devices = self._get_active_devices()
        current_devices = self.get_active_devices()

        new_devices = [item for item in active_devices if item['mac']
                       not in [dev['mac'] for dev in current_devices]]

        removed_devices = [item for item in current_devices if item['mac']
                           not in [dev['mac'] for dev in active_devices]]

        for device in new_devices:
            self._apply('device_signed_on', device)

            if device['mac'] not in self._state['all_devices']:
                self._apply('new_device_connected', device)

        for device in removed_devices:
            self._apply('device_signed_off', device)

    def get_automations(self):
        return [{'type': 'interval', 'interval': 10, 'target_id': self._plugin_id, 'command': 'update_state',
                 'parameters': {}}]

    def _on_device_signed_on(self, event_data):
        self._state['active_devices'].append(event_data)

    def _on_device_signed_off(self, event_data):
        self._state['active_devices'].remove(event_data)

    def _on_new_device_connected(self, event_data):
        self._state['all_devices'].append(event_data['mac'])
