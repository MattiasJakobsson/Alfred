import inspect
import importlib
from os.path import dirname, basename, isfile
import glob
from os.path import relpath
from data_access.database_manager import DatabaseManager
from plugins.parameter_handler import run_python_code
from automation.workflows.workflow_manager import define_workflow, remove_workflow


database_manager = DatabaseManager()
plugin_workflows = {}


def get_available_commands(cls):
    return [{'command': item[0], 'parameters': [p for p in list(inspect.signature(item[1]).parameters) if p != 'self']}
            for item in inspect.getmembers(cls)
            if not item[0].startswith('get_')
            and not item[0].startswith('is_')
            and not item[0] == 'apply_history'
            and not item[0].startswith('_')]


def get_available_queries(cls):
    return [{'query': item[0], 'parameters': [p for p in list(inspect.signature(item[1]).parameters) if p != 'self']}
            for item in inspect.getmembers(cls)
            if (item[0].startswith('get_') or item[0].startswith('is_'))
            and not item[0] == 'get_automations']


def get_all_plugin_modules():
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

        plugin_module = importlib.import_module(name, package='plugins')

        result.append({'name': name, 'module': plugin_module})

    return result


def get_available_plugins():
    modules = get_all_plugin_modules()

    result = []

    for plugin_module in modules:
        settings = plugin_module['module'].get_available_settings() \
            if hasattr(plugin_module['module'], 'get_available_settings') else []

        plugin_type = plugin_module['module'].get_type()

        result.append({'type': plugin_module['name'],
                       'settings': settings,
                       'commands': get_available_commands(plugin_type),
                       'queries': get_available_queries(plugin_type)})

    return result


def auto_detect_plugins():
    current_plugins = database_manager.get_all('plugins')

    modules = get_all_plugin_modules()

    for plugin_module in modules:
        if not hasattr(plugin_module['module'], 'auto_detect'):
            continue

        current_module_plugins = [SettingsManager(plugin['settings']) for plugin in current_plugins
                                  if plugin['type'] == plugin_module['name']]

        new_plugins = plugin_module['module'].auto_detect(current_module_plugins)

        for plugin in new_plugins:
            add_plugin({
                'type': plugin_module['name'],
                'settings': plugin['settings'],
                'title': plugin['title']
            })


def add_plugin(plugin):
    result = database_manager.insert('plugins', plugin)

    added_plugin = database_manager.get_by_id('plugins', result)

    bootstrap_plugin(added_plugin)

    return result


def remove_plugin(plugin_id):
    if isinstance(plugin_id, str):
        plugin_id = database_manager.get_by_condition('plugins', lambda item: item['title'] == plugin_id).eid

    workflows = plugin_workflows[plugin_id] if plugin_id in plugin_workflows else []

    for workflow_id in workflows:
        remove_workflow(workflow_id)

    database_manager.delete('plugins', plugin_id)


def build_plugin_data(plugin):
    plugin_module = importlib.import_module(plugin['type'], package='plugins')

    plugin_type = plugin_module.get_type()

    return {
        'id': plugin.eid,
        'title': plugin['title'],
        'settings': plugin['settings'],
        'availableCommands': get_available_commands(plugin_type),
        'availableQueries': get_available_queries(plugin_type)
    }


def bootstrap_plugin(plugin):
    plugin_module = importlib.import_module(plugin['type'], package='plugins')

    instance = plugin_module.get_type()(plugin.eid, SettingsManager(plugin['settings']))

    if hasattr(instance, 'get_automations'):
        for automation in instance.get_automations():
            workflow_id = define_workflow(automation['definition'], automation['triggers'], store=False)

            if plugin.eid in plugin_workflows:
                plugin_workflows[plugin.eid] += [workflow_id]
            else:
                plugin_workflows[plugin.eid] = [workflow_id]


def bootstrap():
    plugins = database_manager.get_all('plugins')

    for plugin in plugins:
        bootstrap_plugin(plugin)


def get_plugin(plugin_id):
    plugin = database_manager.get_by_id('plugins', plugin_id) if not isinstance(plugin_id, str) \
        else database_manager.get_by_condition('plugins', lambda item: item['title'] == plugin_id)

    if plugin is None:
        return None

    plugin_module = importlib.import_module(plugin['type'], package='plugins')

    instance = plugin_module.get_type()(plugin.eid, SettingsManager(plugin['settings']))

    instance.apply_history(plugin['state'] if 'state' in plugin else None)

    return instance


def get_plugin_type(plugin_id):
    plugin = database_manager.get_by_id('plugins', plugin_id) if not isinstance(plugin_id, str) \
        else database_manager.get_by_condition('plugins', lambda item: item['title'] == plugin_id)

    return plugin['type'] if plugin is not None and 'type' in plugin else None


def execute_command(plugin_id, command, parameters):
    plugin_instance = get_plugin(plugin_id)

    method = getattr(plugin_instance, command)

    arguments = [parameters[p] if p in parameters else None
                 for p in list(inspect.signature(method).parameters) if p != 'self']

    method(*arguments)


def get_query_result(plugin_id, query, parameters):
    plugin_instance = get_plugin(plugin_id)

    method = getattr(plugin_instance, query)

    arguments = [parameters[p] if p in parameters else None
                 for p in list(inspect.signature(method).parameters) if p != 'self']

    return method(*arguments)


class SettingsManager:
    def __init__(self, settings):
        self.settings = settings

    def get_setting(self, setting):
        return run_python_code(self.settings[setting], local_dict={'get_plugin': get_plugin,
                                                                   'query': get_query_result})
