from plugins.parameter_handler import run_python_code
from automation.event_publisher import subscribe


def execute(config, state, step_executed):
    event_name = run_python_code(config['event_name'], local_dict={'state': state})

    def trigger(event_data):
        subscription['dispose']()

        step_executed(event_data)

    subscription = subscribe(event_name, trigger)
