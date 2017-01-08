from waitress import serve
from api.app import configure
from automation import automation_manager
from plugins.plugin_manager import execute_command


automation_manager.bootstrap(execute_command)

api = configure()

serve(api, listen='*:8000')
