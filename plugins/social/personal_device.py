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

    def _subscribe_to_device_signed_on(self, event_data):
        mac = self._get_setting('mac_address')

        if mac == event_data['mac']:
            self._apply('person_signed_on', self.get_person())

    def _subscribe_to_device_signed_off(self, event_data):
        mac = self._get_setting('mac_address')

        if mac == event_data['mac']:
            self._apply('person_signed_off', self.get_person())
