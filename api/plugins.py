from plugins.plugin_manager import get_available_plugins, execute_command, get_query_result, add_plugin, \
    build_plugin_data, auto_detect_plugins
import json
from data_access.database_manager import DatabaseManager


def bootstrap(application):
    plugin_list = PluginList()
    plugin_command = PluginCommand()
    plugin_query = PluginQuery()
    available_plugins = AvailablePlugins()
    auto_detect = AutoDetect()

    application.add_route('/plugins', plugin_list)
    application.add_route('/plugins/{plugin_id}/commands/{command}', plugin_command)
    application.add_route('/plugins/{plugin_id}/queries/{query}', plugin_query)
    application.add_route('/plugins/available', available_plugins)
    application.add_route('/plugins/autodetect', auto_detect)


class AutoDetect:
    def on_post(self, req, resp):
        auto_detect_plugins()

        resp.body = json.dumps({'success': True})


class AvailablePlugins:
    def on_get(self, req, resp):
        plugins = get_available_plugins()

        resp.body = '%s(%s)' % (req.params['jsoncallback'], json.dumps(plugins))


class PluginList:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def on_get(self, req, resp):
        plugins = self.db_manager.get_all('plugins')

        result = [build_plugin_data(plugin) for plugin in plugins]

        resp.body = '%s(%s)' % (req.params['jsoncallback'], json.dumps(result))

    def on_post(self, req, resp):
        data = req.bounded_stream.read().decode()

        plugin_data = json.loads(data)

        plugin = {
            'type': plugin_data['type'],
            'settings': plugin_data['settings'] if 'settings' in plugin_data else {},
            'title': plugin_data['title']
        }

        add_plugin(plugin)

        resp.body = json.dumps({'success': True})


class PluginCommand:
    def on_post(self, req, resp, plugin_id, command):
        data = json.loads(req.bounded_stream.read().decode())

        parameters = data['parameters'] if 'parameters' in data else {}

        execute_command(int(plugin_id), command, parameters)

        resp.body = json.dumps({'success': True})


class PluginQuery:
    def on_post(self, req, resp, plugin_id, query):
        data = json.loads(req.bounded_stream.read().decode())

        parameters = data['parameters'] if 'parameters' in data else {}

        result = get_query_result(int(plugin_id), query, parameters)

        resp.body = json.dumps(result)
