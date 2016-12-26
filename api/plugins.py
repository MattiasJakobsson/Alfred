from plugins.plugin_manager import get_available_plugins, execute_command, get_query_result
import json
from data_access.database_manager import DatabaseManager


def bootstrap(application):
    plugin_list = PluginList()
    plugin_command = PluginCommand()
    plugin_query = PluginQuery()
    available_plugins = AvailablePlugins()

    application.add_route('/plugins', plugin_list)
    application.add_route('/plugins/{id}/commands/{command}', plugin_command)
    application.add_route('/plugins/{id}/queries/{query}', plugin_query)
    application.add_route('/plugins/available', available_plugins)


class AvailablePlugins:
    def on_get(self, resp):
        plugins = get_available_plugins()

        resp.body = json.dumps(plugins)


class PluginList:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def on_get(self, resp):
        result = self.db_manager.get_all('plugins')

        resp.body = json.dumps(result)

    def on_post(self, req, resp):
        data = req.bounded_stream.read().decode()

        result = self.db_manager.insert('plugins', json.loads(data))

        resp.body = str(result)


class PluginCommand:
    def on_post(self, req, resp):
        plugin_id = req.params['id']
        command = req.params['command']

        execute_command(plugin_id, command)

        resp.body = 'Success'


class PluginQuery:
    def on_get(self, req, resp):
        plugin_id = req.params['id']
        query = req.params['query']

        result = get_query_result(plugin_id, query)

        resp.body = json.dumps(result)
