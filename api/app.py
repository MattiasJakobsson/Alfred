import falcon
from falcon_cors import CORS
from .plugins import bootstrap


def configure():
    cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)

    api = falcon.API(middleware=[cors.middleware])

    bootstrap(api)

    return api
