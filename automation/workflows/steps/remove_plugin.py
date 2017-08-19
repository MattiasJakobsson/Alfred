from plugins.parameter_handler import run_python_code
from plugins.plugin_manager import remove_plugin, get_plugin_type


def get_available_settings():
    return ['plugin_id', 'plugin_type']


def execute(config, state, step_executed):
    plugin_id = config['plugin_id']

    if isinstance(config['plugin_id'], str):
        plugin_id = run_python_code(plugin_id, local_dict={'state': state})

    parsed_plugin_id = ignore_exception(ValueError, plugin_id)(int)(plugin_id)

    plugin_type = get_plugin_type(parsed_plugin_id)

    expected_plugin_type = run_python_code(config['plugin_type'], local_dict={'state': state}) \
        if 'plugin_type' in config else None

    if plugin_type is None or (expected_plugin_type is not None and expected_plugin_type != plugin_type):
        return

    remove_plugin(parsed_plugin_id)

    step_executed({})


def ignore_exception(ignore_exception_type, default_val=None):
    def dec(function_to_execute):
        def _dec(*args, **kwargs):
            try:
                return function_to_execute(*args, **kwargs)
            except ignore_exception_type:
                return default_val

        return _dec

    return dec
