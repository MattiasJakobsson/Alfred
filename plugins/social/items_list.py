from plugins.plugin_base import PluginBase


def get_available_settings():
    return []


def get_type():
    return ItemsList


class ItemsList(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager, default_state={'items': []})

    def add_item(self, item):
        self._apply('item_added_to_list', {'list': self._plugin_id, 'item': item})

    def remove_item(self, item):
        self._apply('item_removed_from_list', {'list': self._plugin_id, 'item': item})

    def get_items(self):
        return self._state['items']

    def _on_item_added_to_list(self, event_data):
        self._state['items'] += [event_data['item']]

    def _on_item_removed_from_list(self, event_data):
        self._state['items'].remove(event_data['item'])
