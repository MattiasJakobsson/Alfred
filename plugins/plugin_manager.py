import inspect
import importlib
from os.path import dirname, basename, isfile
import glob
from os.path import relpath
from data_access.database_manager import DatabaseManager
from plugins.parameter_handler import run_python_code


database_manager = DatabaseManager()


def get_available_commands(cls):
    return [(item[0], [p for p in list(inspect.signature(item[1]).parameters) if not p == 'self'])
            for item in inspect.getmembers(cls)
            if not item[0].startswith('get_') and not item[0].startswith('_')]


def get_available_queries(cls):
    return [(item[0], [p for p in list(inspect.signature(item[1]).parameters) if not p == 'self'])
            for item in inspect.getmembers(cls)
            if item[0].startswith('get_')]


def get_available_plugins():
    plugin_path = dirname(__file__)

    directories = [item for item in glob.glob('%s/*/' % plugin_path) if '__pycache__' not in item]

    plugins = []

    for directory in directories:
        modules = glob.glob('%s/*.py' % directory)

        plugins += [f for f in modules if isfile(f)]

    result = []

    for plugin in plugins:
        path = dirname(relpath(plugin, plugin_path))
        name = '.%s.%s' % (path.replace('\\', '.'), basename(plugin)[:-3])

        module = importlib.import_module(name, package='plugins')

        settings = module.get_available_settings() if hasattr(module, 'get_available_settings') else []
        plugin_type = module.get_type()

        result.append({'type': name, 'settings': settings, 'commands': get_available_commands(plugin_type),
                       'queries': get_available_queries(plugin_type)})

    return result


def boostrap():
    plugins = database_manager.get_all('plugins')

    for plugin in plugins:
        module = importlib.import_module(plugin['type'], package='plugins')

        if hasattr(module, 'bootstrap'):
            module.bootstrap(plugin)


def _get_plugin_instance(plugin_id):
    plugin = database_manager.get_by_id('plugins', plugin_id)

    module = importlib.import_module(plugin['type'], package='plugins')

    return module.get_type()(SettingsManager(plugin['settings']))


def execute_command(plugin_id, command):
    plugin_instance = _get_plugin_instance(plugin_id)

    getattr(plugin_instance, command)()


def get_query_result(plugin_id, query):
    plugin_instance = _get_plugin_instance(plugin_id)

    return getattr(plugin_instance, query)()


class SettingsManager:
    def __init__(self, settings):
        self.settings = settings

    def get_setting(self, setting):
        return run_python_code(self.settings[setting], local_dict={'get_plugin': _get_plugin_instance,
                                                                   'query': get_query_result})
