from plugins.plugin_manager import get_available_plugins
import json
from data_access.database_manager import DatabaseManager


class PluginList:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def on_get(self, req, resp):
        plugins = get_available_plugins()

        resp.body = json.dumps(plugins)

    def on_post(self, req, resp):
        data = json.load(req.bounded_stream)

        self.db_manager.insert('plugins', data)

        resp.body = 'Added'
