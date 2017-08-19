from plugins.parameter_handler import run_python_code
import datetime
from automation.scheduler import add_job


def get_available_settings():
    return ['minutes']


def execute(config, state, step_executed):
    minutes = run_python_code(config['minutes'], local_dict={'state': state})

    execute_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

    def done():
        step_executed({})

        job.remove()

    job = add_job(done, 'date', run_date=execute_time)
