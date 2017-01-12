from automation.event_publisher import publish_event


def execute(config, state, step_executed):
    publish_event('workflow_finished', {'workflow_id': config['workflow_id'], 'state': state})

    step_executed({})
