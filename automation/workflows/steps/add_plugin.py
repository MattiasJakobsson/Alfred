from plugins.parameter_handler import run_python_code
from plugins.plugin_manager import add_plugin


def get_available_settings():
    return ['title', 'plugin_type', 'settings']


def execute(config, state, step_executed):
    def parse_settings_data(item):
        for k, v in item.items():
            if isinstance(v, dict):
                parse_settings_data(v)
            if isinstance(v, str):
                item[k] = run_python_code(v, local_dict={'state': state})

    settings = config['settings'] if 'settings' in config \
                                     and config['settings'] is not None \
                                     and isinstance(config['settings'], dict) \
        else {}

    parse_settings_data(settings)

    plugin = {
        'title': run_python_code(config['title'], local_dict={'state': state}),
        'type': run_python_code(config['plugin_type'], local_dict={'state': state}),
        'settings': settings
    }

    plugin_id = add_plugin(plugin)

    step_executed({'plugin_id': plugin_id})
