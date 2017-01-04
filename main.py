from waitress import serve
from api.app import configure
from plugins.plugin_manager import boostrap
from automation import automation_manager


boostrap()

automation_manager.bootstrap()

api = configure()

serve(api, listen='*:8000')
