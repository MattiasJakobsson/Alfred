from bs4 import BeautifulSoup
import requests


def get_available_settings():
    return ['login_user', 'login_password']


def get_type():
    return TilginRouter


class TilginRouter:
    def __init__(self, plugin_id, settings_manager):
        self.plugin_id = plugin_id
        self.settings_manager = settings_manager

    def _sign_in(self):
        login_user = self.settings_manager.get_setting(self.plugin_id, 'login_user')
        login_password = self.settings_manager.get_setting(self.plugin_id, 'login_password')

        payload = {'__formtok': '', '__user': login_user, '__auth': 'login',
                   '__pass': login_password}

        response = requests.post('http://192.168.1.1/', data=payload)

        return response.cookies

    def get_active_devices(self):
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

    def get_ip_from_mac(self, mac_address):
        devices = self.get_active_devices()

        items = [item for item in devices if 'mac' in item and item['mac'] == mac_address]

        return items[0]['ip']
