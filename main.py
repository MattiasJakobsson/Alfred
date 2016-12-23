from components.entertainment.viera_tv.tv_api import TvApi

tv = TvApi().find_tv('BC:30:7E:B9:6C:AB')

tv.power()
