from automation.event_publisher import publish_event
import logging


def execute(config, state, step_executed):
    logging.info('Finishing workflow with config: %s and state: %s' % (str(config), str(state)))

    publish_event('workflow_finished', {'state': state})

    step_executed({})
