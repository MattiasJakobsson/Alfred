import inspect
import importlib
from os.path import dirname, basename, isfile
import glob
from os.path import relpath


def get_available_commands(cls):
    return [item[0] for item in inspect.getmembers(cls) if not item[0].startswith('get_')
            and not item[0].startswith('_')]


def get_available_queries(cls):
    return [item[0] for item in inspect.getmembers(cls) if item[0].startswith('get_')]


def get_available_plugins():
    plugin_path = dirname(__file__)

    directories = [item for item in glob.glob('%s/*/' % plugin_path) if '__pycache__' not in item]

    plugins = []

    for directory in directories:
        modules = glob.glob('%s/*.py' % directory)

        plugins += [f for f in modules if isfile(f)]

    result = []

    for plugin in plugins:
        name = basename(plugin)[:-3]
        path = dirname(relpath(plugin, plugin_path))

        module = importlib.import_module('.%s.%s' % (path.replace('\\', '.'), name), package='plugins')

        settings = module.get_available_settings()
        plugin_type = module.get_type()

        result.append({'name': name, 'settings': settings, 'commands': get_available_commands(plugin_type),
                       'queries': get_available_queries(plugin_type)})

    return result


class SettingsManager:
    def __init__(self, settings):
        self.settings = settings

    def get_setting(self, plugin_id, setting):
        return self.settings[plugin_id][setting]
