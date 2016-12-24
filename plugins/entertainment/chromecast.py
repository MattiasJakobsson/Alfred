def get_available_settings():
    return ['name']


def get_type():
    return ChromecastDevice


class ChromecastDevice:
    def __init__(self, plugin_id, settings_manager):
        self.plugin_id = plugin_id
        self.settings_manager = settings_manager
