from plugins.plugin_base import PluginBase


def get_available_settings():
    return ['name']


def get_type():
    return ChromecastDevice


class ChromecastDevice(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager)
