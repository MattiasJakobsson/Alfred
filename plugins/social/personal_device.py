from plugins.plugin_base import PluginBase


def get_available_settings():
    return ['mac_address', 'name', 'email']


def get_type():
    return PersonalDevice


class PersonalDevice(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager, default_state={'is_online': False})

    def get_person(self):
        return {'name': self._get_setting('name'), 'email': self._get_setting('email')}

    def get_online_status(self):
        return self._state['is_online']

    def get_automations(self):
        return [{
            'definition': {'initial_step': {
                'id': 'handle_%s_signed_on' % self._get_setting('name'),
                'type': '.workflows.steps.execute_plugin_command',
                'plugin_id': self._plugin_id,
                'command': 'handle_device_signed_on',
                'parameters': {'event_data': '[??state["initial_state"]["data"]??]'}
            }},
            'triggers': [{'type': '.workflows.triggers.event_listener_trigger', 'subscribe_to': 'device_signed_on'}]
        },
            {
                'definition': {'initial_step': {
                    'id': 'handle_%s_signed_off' % self._get_setting('name'),
                    'type': '.workflows.steps.execute_plugin_command',
                    'plugin_id': self._plugin_id,
                    'command': 'handle_device_signed_off',
                    'parameters': {'event_data': '[??state["initial_state"]["data"]??]'}
                }},
                'triggers': [{'type': '.workflows.triggers.event_listener_trigger',
                              'subscribe_to': 'device_signed_off'}]
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

    def _on_person_signed_on(self, _):
        self._state['is_online'] = True

    def _on_person_signed_off(self, _):
        self._state['is_online'] = False
