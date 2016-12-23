def get_name():
    return 'Chromecast'


def get_default_settings():
    return {'name': ''}


def get_type():
    return ChromecastDevice


class ChromecastDevice:
    def __init__(self, settings):
        self.name = settings['name']
