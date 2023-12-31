'''

This program report TFA WeatherHub (https://www.tfa-dostmann.de/en/produkte/weather-hub/) data to
Met Office (meteorologic weather service) in UK https://www.metoffice.gov.uk/.

The program collects weather observations data from the TFA cloud service https://www.data199.com/.
The format and API is found here; https://mobile-alerts.eu/info/public_server_api_documentation.pdf

This program just collects outdoor temp and wind metrics, but you may collect other data depending on your configuration.

The observations are reported to the Met Office cloud service. For that you have to
1) create an Met Office account(https://register.metoffice.gov.uk/WaveRegistrationClient/public/register.do?service=weatherobservations)
2) create and define your weather station site. Instructions can be found here; https://about.metservice.com/our-company/your-weather/add-your-own-weather-station/
3) It's is a bit unclear what interface to use when reporting observations to the MET Office service. The one that seems to work is http://wow.metoffice.gov.uk/automaticreading.
   The interface is described here; https://wow.metoffice.gov.uk/support/dataformats

   There is also another interface that allows you to report observation, however those observation reported does not seem to be connected with https://wow.metoffice.gov.uk/ information.
   If you however like to explore that interface you can find more about it at  the Met development portal https://mowowprod.portal.azure-api.net/ where you have to another account.
   See https://mowowprod.portal.azure-api.net/documentation/how-to-obtain-a-subscription-key for futher details. The REST API for uploading data to the Met Office Azure service are found here;
https://mowowprod.portal.azure-api.net/documentation/table-of-contents


'''
import time

import requests
import datetime
from datetime import timezone
import urllib.parse
import json

windmeter_id = "0B6025223DD2"
outtemp_id = "026A795CD3B4"
latitude = 60.419572
longitude = 19.917539


def timnow() -> str:
    _tim = datetime.datetime.now()
    return _tim.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def timDiff( time_stamp: int ) -> int:
    _date_time = datetime.datetime.fromtimestamp( time_stamp )
    _now = datetime.datetime.now();
    _diff = _now - _date_time;
    return _diff.seconds;


def log( msg : str):
    with open('tfa-met.log', 'a', encoding="utf-8") as fd:
      fd.write( timnow() + "  " + msg + "\n");


def getTfaData(auth_keys: dict)  -> dict:
    url = 'https://www.data199.com/api/pv1/device/lastmeasurement'

    devices=f"{windmeter_id},{outtemp_id}"

    rqst_data = {"deviceids" : devices, "phoneid" : auth_keys['phone_id'] }
    response = requests.post( url , json= rqst_data )
    json_str = response.content.decode('utf8').replace("'", '"')
    data = json.loads(json_str)
    log("TFA data: " + json_str )
    return data


# YYYY-mm-DD HH:mm:ss
def toUTCDateTime() ->str:
    date_time = datetime.datetime.now(tz=timezone.utc)
    timstr = date_time.strftime("%Y-%m-%d %H:%M:%S")
    return urllib.parse.quote(timstr)

def getDeviceData( tfa_data : dict, id : str ):
    arr = tfa_data["devices"]
    for dev in arr:
        if (dev["deviceid"] == id):
            return dev
    return None

def reportToWow( tfa_data : dict, auth_keys: dict):
    wind_dev = getDeviceData( tfa_data, windmeter_id)
    temp_dev = getDeviceData( tfa_data, outtemp_id)
    if wind_dev:
        wind_data = wind_dev["measurement"]
        wind_data_age_sec = timDiff(wind_dev["lastseen"])
    if temp_dev:
        temp_data = temp_dev["measurement"]
        temp_data_age_sec = timDiff(temp_dev["lastseen"])

    if wind_dev or temp_dev:
        url = "http://wow.metoffice.gov.uk/automaticreading"
        url += "?siteid=" + auth_keys['site_id']
        url += "&siteAuthenticationKey=" + auth_keys['site_auth_key']
        url += "&dateutc=" + toUTCDateTime()

        if wind_dev and (wind_data_age_sec < 7200):
            url += "&winddir=" + str(int((22.5 * wind_data["wd"])))
            url += "&windspeedmph=" + str(int(float(wind_data["ws"]) * 2.23694))
            url += "&windgustmph=" + str(int((float(wind_data["wg"]) * 2.23694)))
        if temp_data and (temp_data_age_sec < 7200):
            url += "&tempf=" + str(int((float(temp_data["t1"]) * (9/5)) + 32))
        url += "&softwaretype=TA-bridge-v1.0"

        response = requests.get( url )
        if (response.status_code >= 200) and (response.status_code <= 299):
            json_response_str = response.content.decode('utf8').replace("'", '"')
            log("wow response: " + json_response_str )
        else:
            log(" %%%% wow reporting failure status: " + str(response.status_code) + " reason: " + response.reason )
    else:
        log("failed to retreive data from TFA")


def loadAuthKeys() -> dict:
    fd = open('auth_keys.json')
    return json.load(fd)


def main():
    log("*** start TFA service ***");
    auth_keys = loadAuthKeys()
    log("loaded auth data " + json.dumps( auth_keys))
    while(True):
        tfa_data = getTfaData(auth_keys)
        reportToWow( tfa_data, auth_keys )
        time.sleep(1800) # Sleep 30 min



if __name__ == '__main__':
    main()