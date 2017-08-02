from plugins.parameter_handler import run_python_code
from plugins.plugin_manager import remove_plugin


def execute(config, state, step_executed):
    plugin_id = config['plugin_id']

    if isinstance(config['plugin_id'], str):
        plugin_id = run_python_code(plugin_id, local_dict={'state': state})

    parsed_plugin_id = ignore_exception(ValueError, plugin_id)(int)(plugin_id)

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
