from waitress import serve
from api.app import configure
from plugins.plugin_manager import boostrap

boostrap()

api = configure()

serve(api, listen='*:8000')
