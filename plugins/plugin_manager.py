import inspect
import importlib
from os.path import dirname, basename, isfile
import glob
from os.path import relpath
from data_access.database_manager import DatabaseManager
from plugins.parameter_handler import run_python_code
from automation.scheduler import add_job


database_manager = DatabaseManager()


def get_available_commands(cls):
    return [{'command': item[0], 'parameters': [p for p in list(inspect.signature(item[1]).parameters) if p != 'self']}
            for item in inspect.getmembers(cls)
            if not item[0].startswith('get_') and not item[0] == 'apply_history'
            and not item[0] == 'ping' and not item[0].startswith('_')]


def get_available_queries(cls):
    return [{'query': item[0], 'parameters': [p for p in list(inspect.signature(item[1]).parameters) if p != 'self']}
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


def build_plugin_data(plugin):
    module = importlib.import_module(plugin['type'], package='plugins')

    plugin_type = module.get_type()

    return {
        'id': plugin.eid,
        'title': plugin['title'],
        'settings': plugin['settings'],
        'availableCommands': get_available_commands(plugin_type),
        'availableQueries': get_available_queries(plugin_type)
    }

jobs = {}


def teardown_plugin(plugin):
    if plugin.eid in jobs:
        jobs[plugin.eid].remove()

        del jobs[plugin.eid]


def bootstrap_plugin(plugin):
    module = importlib.import_module(plugin['type'], package='plugins')

    instance = module.get_type()(plugin.eid, SettingsManager(plugin['settings']))

    instance.apply_history(plugin['state'] if 'state' in plugin else None)

    def handle_ping():
        plugin_instance = _get_plugin_instance(plugin.eid)

        plugin_instance.ping()

    if hasattr(instance, 'ping'):
        seconds = instance.ping_timeout if hasattr(instance, 'ping_timeout') else 10

        job = add_job(handle_ping, 'interval', seconds=seconds)

        jobs[plugin.eid] = job


def boostrap():
    plugins = database_manager.get_all('plugins')

    for plugin in plugins:
        bootstrap_plugin(plugin)


def _get_plugin_instance(plugin_id):
    plugin = database_manager.get_by_id('plugins', plugin_id)

    module = importlib.import_module(plugin['type'], package='plugins')

    instance = module.get_type()(plugin.eid, SettingsManager(plugin['settings']))

    instance.apply_history(plugin['state'] if 'state' in plugin else None)

    return instance


def execute_command(plugin_id, command, parameters):
    plugin_instance = _get_plugin_instance(plugin_id)

    method = getattr(plugin_instance, command)

    arguments = [parameters[p] if p in parameters else None
                 for p in list(inspect.signature(method).parameters) if p != 'self']

    method(*arguments)


def get_query_result(plugin_id, query, parameters):
    plugin_instance = _get_plugin_instance(plugin_id)

    method = getattr(plugin_instance, query)

    arguments = [parameters[p] if p in parameters else None
                 for p in list(inspect.signature(method).parameters) if p != 'self']

    return method(*arguments)


class SettingsManager:
    def __init__(self, settings):
        self.settings = settings

    def get_setting(self, setting):
        return run_python_code(self.settings[setting], local_dict={'get_plugin': _get_plugin_instance,
                                                                   'query': get_query_result})
