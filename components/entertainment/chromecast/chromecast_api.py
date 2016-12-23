import pychromecast


class ChromeCastApi:
    def find_active_devices(self):
        return pychromecast.get_chromecasts_as_dict()

    def find_device(self, friendly_name):
        device = pychromecast.get_chromecast(friendly_name=friendly_name)

        device.wait()

        return device
