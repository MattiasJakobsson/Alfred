from automation.scheduler import add_job
from automation.event_publisher import publish_event


def get_available_settings():
    return ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_date', 'end_date',
            'timezone']


def set_up(workflow_id, data):
    def start_workflow():
        publish_event('new_workflow_instance_requested', {'workflow_id': workflow_id, 'initial_state': {}})

    job = add_job(start_workflow, 'cron', **data)

    return {
        'dispose': lambda: job.remove()
    }
