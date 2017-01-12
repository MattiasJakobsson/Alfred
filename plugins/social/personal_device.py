from plugins.plugin_base import PluginBase
import uuid


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
        return [{
            'definition': {'initial_step': {
                'id': str(uuid.uuid4()),
                'type': '.workflows.steps.execute_plugin_command',
                'plugin_id': self._plugin_id,
                'command': 'handle_device_signed_on',
                'parameters': {}
            }},
            'triggers': [{'type': '.workflows.triggers.event_listener_trigger', 'subscribe_to': 'device_signed_on'}]
        },
            {
                'definition': {'initial_step': {
                    'id': str(uuid.uuid4()),
                    'type': '.workflows.steps.execute_plugin_command',
                    'plugin_id': self._plugin_id,
                    'command': 'handle_device_signed_off',
                    'parameters': {}
                }},
                'triggers': [{'type': '.workflows.triggers.event_listener_trigger', 'subscribe_to': 'device_signed_off'}]
            }
        ]

    def handle_device_signed_on(self, event_data):
        mac = self._get_setting('mac_address')

        if mac == event_data['mac']:
            self._apply('person_signed_on', self.get_person())

    def handle_device_signed_off(self, event_data):
        mac = self._get_setting('mac_address')

        if mac == event_data['mac']:
            self._apply('person_signed_off', self.get_person())
