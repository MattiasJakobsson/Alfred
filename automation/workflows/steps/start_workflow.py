from automation.event_publisher import publish_event
from plugins.parameter_handler import run_python_code


def get_available_settings():
    return ['workflow_to_execute', 'initial_state']


def execute(config, state, step_executed):
    initial_state = {}

    if 'initial_state' in config:
        for key in config['initial_state']:
            initial_state[key] = run_python_code(config['initial_state'][key], local_dict={'state': state})

    publish_event('new_workflow_instance_requested', {'workflow_id': config['workflow_to_execute'],
                                                      'initial_state': initial_state})

    step_executed({})
