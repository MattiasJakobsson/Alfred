from plugins.parameter_handler import run_python_code
from automation.event_publisher import publish_event


def execute(config, state, step_executed):
    event_name = config['event_name']
    event_data_patterns = config['event_data'] if 'event_data' in config else {}

    event_data = {}

    for key in event_data_patterns:
        event_data[key] = run_python_code(event_data_patterns[key], local_dict={'state': state})

    publish_event(event_name, event_data)

    step_executed({})
