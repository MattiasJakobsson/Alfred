from automation.event_publisher import publish_event


class PluginBase:
    def __init__(self, plugin_id, settings_manager):
        self._plugin_id = plugin_id
        self._settings_manager = settings_manager

    def _apply(self, event_name, event_data):
        apply_method = getattr(self, '_on_%s' % event_name)

        if apply_method:
            apply_method(event_data)

        publish_event('plugins-%s' % str(self._plugin_id), event_name, event_data)

    def apply_history(self, events):
        for event in events:
            apply_method = getattr(self, '_on_%s' % event['name'])

            if apply_method:
                apply_method(event['data'])

    def _get_setting(self, setting_name):
        return self._settings_manager.get_setting(setting_name)
