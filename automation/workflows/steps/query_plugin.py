from plugins.plugin_manager import get_query_result
from plugins.parameter_handler import run_python_code


def get_available_settings():
    return ['plugin_id', 'query', 'parameters']


def execute(config, state, step_executed):
    plugin_id = run_python_code(config['plugin_id'], local_dict={'state': state}) \
        if isinstance(config['plugin_id'], str) else config['plugin_id']

    query = run_python_code(config['query'], local_dict={'state': state})
    parameter_patterns = config['parameters'] if 'parameters' in config else {}

    parameters = {}

    for key in parameter_patterns:
        parameters[key] = run_python_code(parameter_patterns[key], local_dict={'state': state})

    step_executed(get_query_result(plugin_id, query, parameters))
