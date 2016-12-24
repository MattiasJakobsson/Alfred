import falcon
from waitress import serve

from .registration import Registration
from .plugins import PluginList

api = application = falcon.API()

plugin_list = PluginList()

api.add_route('/plugins', plugin_list)

registration = Registration()
api.add_route('/registration', registration)

serve(api, listen='*:8000')
