from automation.event_publisher import publish_event, subscribe


def get_available_settings():
    return ['mac_address', 'name', 'email']


def get_type():
    return PersonalDevice


class PersonalDevice:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager

    def bootstrap(self):
        def signed_on(evnt):
            mac = self.settings_manager.get_setting('mac_address')

            if mac == evnt['mac']:
                publish_event('personal_device', 'PersonSignedOn', self.get_person())

        def signed_off(evnt):
            mac = self.settings_manager.get_setting('mac_address')

            if mac == evnt['mac']:
                publish_event('personal_device', 'PersonSignedOff', self.get_person())

        subscribe('personal_device', 'DeviceSignedOn', signed_on)
        subscribe('personal_device', 'DeviceSignedOff', signed_off)

    def get_person(self):
        return {'name': self.settings_manager.get_setting('name'), 'email': self.settings_manager.get_setting('email')}
