from plugins.plugin_manager import get_available_plugins
import json


class PluginList:
    def on_get(self, req, resp):
        plugins = get_available_plugins()

        resp.body = json.dumps(plugins)
