from automation.event_publisher import subscribe, publish_event


def set_up(workflow_id, data):
    event_name = data['subscribe_to']

    def start_workflow(event_data):
        publish_event('new_workflow_instance_requested', {'workflow_id': workflow_id, 'initial_state': {
            'event_name': event_name,
            'data': event_data
        }})

    subscription = subscribe(event_name, start_workflow)

    return {
        'dispose': lambda: subscription['dispose']()
    }
