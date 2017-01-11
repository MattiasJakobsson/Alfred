from plugins.plugin_base import PluginBase
import requests
import json


def get_available_settings():
    return ['ip']


def get_type():
    return ThinkingCleanerRoomba


class ThinkingCleanerRoomba(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager, default_state={'cleaner_state': '', 'cleaning': False})

    def get_status(self):
        return json.loads(requests.get('http://%s/status.json' % self._get_setting('ip')).text)['status']

    def start_cleaning(self):
        requests.get('http://%s/command.json?command=clean' % self._get_setting('ip'))

    def start_spot_cleaning(self):
        requests.get('http://%s/command.json?command=spot' % self._get_setting('ip'))

    def schedule_cleaning(self, minutes):
        requests.get('http://%s/command.json?command=CleanDelay&minutes=%s' % (self._get_setting('ip'), minutes))

    def start_max_cleaning(self):
        requests.get('http://%s/command.json?command=max' % self._get_setting('ip'))

    def stop_cleaning(self):
        requests.get('http://%s/command.json?command=dock' % self._get_setting('ip'))

    def find_cleaner(self):
        requests.get('http://%s/command.json?command=find_me' % self._get_setting('ip'))

    def leave_home(self):
        requests.get('http://%s/command.json?command=leavehomebase' % self._get_setting('ip'))

    def update_state(self):
        active_states = self.get_status()

        if self._state['cleaner_state'] != active_states['cleaner_state']:
            self._apply('cleaner_changed_state', {'new_state': self._state['cleaner_state']})

        if self._state['cleaning'] != active_states['cleaning']:
            if active_states['cleaning']:
                self._apply('cleaner_started_cleaning', {})
            else:
                self._apply('cleaner_stopped_cleaning', {})

    def get_automations(self):
        return [{'type': 'interval', 'interval': 10, 'target_id': self._plugin_id, 'command': 'update_state',
                 'parameters': {}}]

    def _on_cleaner_changed_state(self, event_data):
        self._state['cleaner_state'] = event_data['new_state']

    def _on_cleaner_started_cleaning(self, event_data):
        self._state['cleaning'] = True

    def _on_cleaner_stopped_cleaning(self, event_data):
        self._state['cleaning'] = False
