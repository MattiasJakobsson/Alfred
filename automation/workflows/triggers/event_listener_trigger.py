from automation.event_publisher import subscribe, publish_event


def set_up(workflow_id, data):
    def start_workflow(event_data):
        publish_event('new_workflow_instance_requested', {'workflow_id': workflow_id, 'initial_state': event_data})

    subscribe(data['subscribe_to'], start_workflow)
