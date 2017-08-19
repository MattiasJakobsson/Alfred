import logging


def execute(config, state, step_executed):
    logging.info('Finishing workflow with config: %s and state: %s' % (str(config), str(state)))

    step_executed({})
