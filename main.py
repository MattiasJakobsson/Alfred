from waitress import serve
from api.app import configure
import automation.workflows.workflow_manager
import logging


logging.basicConfig(level=logging.INFO)

logging.info('Starting application')

automation.workflows.workflow_manager.bootstrap()

api = configure()

logging.info('Starting web api')

serve(api, listen='*:8000')

logging.info('Stopping application')

automation.workflows.workflow_manager.shut_down()

logging.info('Application shut down')
