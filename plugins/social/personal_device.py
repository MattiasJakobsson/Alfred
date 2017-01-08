from plugins.plugin_base import PluginBase


def get_available_settings():
    return ['mac_address', 'name', 'email']


def get_type():
    return PersonalDevice


class PersonalDevice(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager)

    def get_person(self):
        return {'name': self._get_setting('name'), 'email': self._get_setting('email')}

    def get_automations(self):
        return [{'type': 'subscription', 'subscribe_to': 'device_signed_on', 'target_id': self._plugin_id,
                 'command': 'handle_device_signed_on', 'parameters': {'event_data': {}}},
                {'type': 'subscription', 'subscribe_to': 'device_signed_off', 'target_id': self._plugin_id,
                 'command': 'handle_device_signed_off', 'parameters': {'event_data': {}}}
                ]

    def handle_device_signed_on(self, event_data):
        mac = self._get_setting('mac_address')

        if mac == event_data['mac']:
            self._apply('person_signed_on', self.get_person())

    def handle_device_signed_off(self, event_data):
        mac = self._get_setting('mac_address')

        if mac == event_data['mac']:
            self._apply('person_signed_off', self.get_person())
