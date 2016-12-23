from bs4 import BeautifulSoup
import requests


class RouterApi:
    def __init__(self):
        payload = {'__formtok': '', '__user': 'admin', '__auth': 'login',
                   '__pass': 'h7wan62s'}
        url = 'http://192.168.1.1/'

        response = requests.post(url, data=payload)

        self.cookies = response.cookies

    def get_connected_devices(self):
        response = requests.get('http://192.168.1.1/status/lan_clients/', cookies=self.cookies)

        soup = BeautifulSoup(response.text, 'lxml')

        clients_box = soup.find(id="content")

        result = []

        for table in clients_box.find_all('tbody'):
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                result.append({'name': columns[0].text, 'mac': columns[1].text, 'ip': columns[2].text,
                               'type': columns[3].text, 'media': columns[4].text})

        return result
