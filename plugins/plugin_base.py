from automation.event_publisher import publish_event
from data_access.database_manager import DatabaseManager


class PluginBase:
    def __init__(self, plugin_id, settings_manager, default_state={}):
        self._plugin_id = plugin_id
        self._settings_manager = settings_manager
        self._state = default_state
        self._database_manager = DatabaseManager()

    def _apply(self, event_name, event_data):
        if hasattr(self, '_on_%s' % event_name):
            apply_method = getattr(self, '_on_%s' % event_name)

            apply_method(event_data)

            self._database_manager.update('plugins', self._plugin_id, {'state': self._state})

        publish_event(event_name, event_data)

    def apply_history(self, state):
        if state is not None:
            self._state = state

    def _get_setting(self, setting_name):
        return self._settings_manager.get_setting(setting_name)
