import requests
from bs4 import BeautifulSoup
from automation.scheduler import add_job

from data_access.cache_manager import cache
from data_access.database_manager import DatabaseManager
from automation.event_publisher import publish_event


def get_available_settings():
    return ['login_user', 'login_password']


def get_type():
    return TilginRouter


class TilginRouter:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.cache = cache.get_cache('tilgin_router', expire=300)
        self.db_manager = DatabaseManager()

    def _get_api_cookies(self):
        login_user = self.settings_manager.get_setting('login_user')
        login_password = self.settings_manager.get_setting('login_password')

        payload = {'__formtok': '', '__user': login_user, '__auth': 'login',
                   '__pass': login_password}

        response = requests.post('http://192.168.1.1/', data=payload)

        self.cookies = response.cookies

        return response.cookies

    def _sign_in(self):
        return self.cache.get(key='cookies', createfunc=self._get_api_cookies)

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

    def bootstrap(self):
        def send_updates():
            active_devices = self._get_active_devices()
            current_devices = self.db_manager.get_all('tilgin_devices')

            new_devices = [item for item in active_devices if item['mac']
                           not in [dev['mac'] for dev in current_devices]]

            removed_devices = [item for item in current_devices if item['mac']
                               not in [dev['mac'] for dev in active_devices]]

            for device in new_devices:
                publish_event('tilginrouter', 'DeviceSignedOn', device)

                self.db_manager.insert('tilgin_devices', device)

            for device in removed_devices:
                publish_event('tilginrouter', 'DeviceSignedOff', device)

                self.db_manager.delete('tilgin_devices', device.eid)

        add_job(send_updates, 'interval', seconds=10)

    def get_active_devices(self):
        return self.db_manager.get_all('tilgin_devices')

    def get_ip_from_mac(self, mac_address):
        devices = self.get_active_devices()

        items = [item for item in devices if 'mac' in item and item['mac'] == mac_address]

        return items[0]['ip']

    def get_is_device_online(self, mac_address):
        devices = self.get_active_devices()

        return mac_address in [item['mac'] for item in devices]
