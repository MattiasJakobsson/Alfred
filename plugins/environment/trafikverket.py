import requests
from plugins.plugin_base import PluginBase
import json


def get_available_settings():
    return ['api_key']


def get_type():
    return Trafikverket


class Trafikverket(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager)

    def _send_request(self, query):
        api_key = self._get_setting('api_key')

        body = '<REQUEST><LOGIN authenticationkey="%s" />%s</REQUEST>' % (api_key, query)

        headers = {
            'Content-Length': str(len(body)),
            'Accept': 'application/json'
        }

        response = requests.post('https://api.trafikinfo.trafikverket.se/v1.2/data.json', data=body, headers=headers)

        return json.loads(response.text)

    def get_all_train_stations(self):
        query = '<QUERY objecttype="TrainStation"> \
                        <FILTER /> \
                  </QUERY>'

        return self._send_request(query)['RESPONSE']['RESULT']

    def get_train_station_messages(self, station):
        query = '<QUERY objecttype="TrainMessage"> \
                    <FILTER> \
                          <EQ name="AffectedLocation" value="' + station + '" /> \
                    </FILTER> \
                    <INCLUDE>StartDateTime</INCLUDE> \
                    <INCLUDE>LastUpdateDateTime</INCLUDE> \
                    <INCLUDE>ExternalDescription</INCLUDE> \
                    <INCLUDE>ReasonCodeText</INCLUDE> \
              </QUERY>'

        return self._send_request(query)['RESPONSE']['RESULT']

    def get_train_departures_for(self, station):
        query = '<QUERY objecttype="TrainAnnouncement" orderby="AdvertisedTimeAtLocation"> \
                    <FILTER> \
                          <AND> \
                                <EQ name="ActivityType" value="Avgang" /> \
                                <EQ name="LocationSignature" value="' + station + '" /> \
                                <OR> \
                                      <AND> \
                                            <GT name="AdvertisedTimeAtLocation" value="$dateadd(-00:15:00)" /> \
                                            <LT name="AdvertisedTimeAtLocation" value="$dateadd(14:00:00)" /> \
                                      </AND> \
                                      <AND> \
                                            <LT name="AdvertisedTimeAtLocation" value="$dateadd(00:30:00)" /> \
                                            <GT name="EstimatedTimeAtLocation" value="$dateadd(-00:15:00)" /> \
                                      </AND> \
                                </OR> \
                          </AND> \
                    </FILTER> \
                    <INCLUDE>AdvertisedTrainIdent</INCLUDE> \
                    <INCLUDE>AdvertisedTimeAtLocation</INCLUDE> \
                    <INCLUDE>TrackAtLocation</INCLUDE> \
                    <INCLUDE>ToLocation</INCLUDE> \
              </QUERY>'

        return self._send_request(query)['RESPONSE']['RESULT']
