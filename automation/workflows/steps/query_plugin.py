from plugins.plugin_manager import get_query_result
from plugins.parameter_handler import run_python_code


def execute(config, state, step_executed):
    plugin_id = config['plugin_id']
    query = config['query']
    parameter_patterns = config['parameters'] if 'parameters' in config else {}

    parameters = {}

    for key in parameter_patterns:
        parameters[key] = run_python_code(parameter_patterns[key], local_dict={'state': state})

    step_executed(get_query_result(plugin_id, query, parameters))
