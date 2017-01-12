from plugins.plugin_base import PluginBase
from wit import Wit


def get_available_settings():
    return ['api_token']


def get_type():
    return WitText


class WitText(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager)

        self._client = Wit(access_token=self._get_setting('api_token'))

    def get_intent(self, text):
        return self._client.message(text)
