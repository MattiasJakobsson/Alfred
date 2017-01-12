from waitress import serve
from api.app import configure
import automation.workflows.workflow_manager


automation.workflows.workflow_manager.bootstrap()

api = configure()

serve(api, listen='*:8000')
