from plugins.plugin_manager import execute_command
from plugins.parameter_handler import run_python_code


def execute(config, state, step_executed):
    plugin_id = config['plugin_id']
    command = config['command']
    parameter_patterns = config['parameters'] if 'parameters' in config else {}

    parameters = {}

    for key in parameter_patterns:
        parameters[key] = run_python_code(parameter_patterns[key], local_dict={'state': state})

    execute_command(plugin_id, command, parameters)

    step_executed({})
