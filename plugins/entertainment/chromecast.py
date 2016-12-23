def get_name():
    return 'Chromecast'


def get_default_settings():
    return {'name': ''}


def get_available_commands():
    return {}


def get_available_queries():
    return {}


def create(settings):
    return ChromecastDevice(settings)


class ChromecastDevice:
    def __init__(self, settings):
        self.settings = settings
