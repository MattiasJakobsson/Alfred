import falcon
from waitress import serve

from .registration import Registration

api = application = falcon.API()

registration = Registration()
api.add_route('/registration', registration)

serve(api, listen='*:8000')
