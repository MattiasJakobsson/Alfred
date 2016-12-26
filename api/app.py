import falcon
from .plugins import bootstrap


def configure():
    api = falcon.API()

    bootstrap(api)

    return api
