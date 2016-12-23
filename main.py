from components.entertainment.marantz_amp.amplifier_api import AmplifierApi

device = AmplifierApi().find_amp('00:06:78:23:72:2E')

device.power()
