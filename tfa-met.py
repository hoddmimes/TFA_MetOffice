'''

This program report TFA WeatherHub (https://www.tfa-dostmann.de/en/produkte/weather-hub/) data to
Met Office (meteorologic weather service) in UK https://www.metoffice.gov.uk/.

The program collects weather observations data from the TFA cloud service https://www.data199.com.
The format and API is found here; https://mobile-alerts.eu/info/public_server_api_documentation.pdf

This program just collects outdoor temp and wind metrics, but you may collect other data depending on your configuration.

The observations are reported to the Met Office cloud service. For that you have to
1) create an Met Office account(https://register.metoffice.gov.uk/WaveRegistrationClient/public/register.do?service=weatherobservations)
2) create and define your weather station site. Instructions can be found here; https://about.metservice.com/our-company/your-weather/add-your-own-weather-station/
3) observation are uploaded to the Met Office cloud service, apparently an Azure service. In order for that you will need to have a 'subscription key' that is obtained
from the Met development portal https://mowowprod.portal.azure-api.net/ where you have to another account. See https://mowowprod.portal.azure-api.net/documentation/how-to-obtain-a-subscription-key
for futher details.

4) the REST API for uploading data to the Met Office Azure service are found here;
https://mowowprod.portal.azure-api.net/documentation/table-of-contents


'''
import time

import requests
import datetime
from datetime import timezone
import json

windmeter_id = "0B6025223DD2"
outtemp_id = "026A795CD3B4"
latitude = 60.419572
longitude = 19.917539


def timnow() -> str:
    _tim = datetime.datetime.now()
    return _tim.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


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


def toUTCDateTime( timestamp : int ) ->str:
    date_time = datetime.datetime.fromtimestamp( timestamp, tz=timezone.utc )
    timstr = date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return timstr

def getDeviceData( tfa_data : dict, id : str ):
    arr = tfa_data["devices"]
    for dev in arr:
        if (dev["deviceid"] == id):
            return dev
    return None

def reportToWow( tfa_data : dict, auth_keys: dict):
    wind_dev = getDeviceData( tfa_data, windmeter_id)
    if wind_dev:
        headers = {'Content-Type': 'application/json','Ocp-Apim-Subscription-Key': auth_keys['subscription_key'],}


        measurement = wind_dev["measurement"]
        utc_date_time = toUTCDateTime( wind_dev["lastseen"] )
        wow_data = {}
        wow_data["SiteId"] = auth_keys['site_id']
        wow_data["SiteAuthenticationKey"] = auth_keys['site_auth_key']
        wow_data["ReportStartDateTime"] = utc_date_time
        wow_data["ReportEndDateTime"] = utc_date_time
        wow_data["Longitude"] = float(longitude)
        wow_data["Latitude"] = float(latitude)
        wow_data["WindDirection"] = 22.5 * measurement["wd"]
        wow_data["WindSpeed_MetrePerSecond"] = float(measurement["ws"])
        wow_data["WindGust_MetrePerSecond"] = float(measurement["wg"])
        wow_data["isPublic"] = True
        wow_data["ObservationType"] = 1
        print( wow_data )

        url = 'https://mowowprod.azure-api.net/api/Observations'

        response = requests.post( url , json= wow_data, headers=headers )
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