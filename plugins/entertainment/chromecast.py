def get_available_settings():
    return ['name']


def get_type():
    return ChromecastDevice


class ChromecastDevice:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
