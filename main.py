from components.entertainment.chromecast.chromecast_api import ChromeCastApi

device = ChromeCastApi().find_device('Tv')

print(device)
