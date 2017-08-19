from plugins.parameter_handler import run_python_code
from plugins.plugin_manager import get_plugin, get_query_result
import logging


def get_available_settings():
    return ['if_statement', 'true_step', 'false_step']


def execute(config, state, step_executed):
    if_result = run_python_code(config['if_statement'], local_dict={'state': state,
                                                                    'get_plugin': get_plugin,
                                                                    'query': get_query_result}) == "True"

    logging.info('If statement "%s" executed with result %s for data %s' %
                 (config['if_statement'], str(if_result), str({'state': state})))

    if if_result:
        logging.info('Finishing step with true_step as next')

        step_executed({'next_step': config['true_step']})
    else:
        logging.info('Finishing step with false_step as next')

        step_executed({'next_step': config['false_step']})
