from automation.scheduler import add_job
from automation.event_publisher import publish_event


def set_up(workflow_id, data):
    def start_workflow():
        publish_event('new_workflow_instance_requested', {'workflow_id': workflow_id, 'initial_state': {}})

    add_job(start_workflow, 'interval', seconds=data['interval'])
