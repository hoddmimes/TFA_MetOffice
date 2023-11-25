# TFA_MetOffice

This program report TFA WeatherHub (https://www.tfa-dostmann.de/en/produkte/weather-hub/) data to
Met Office (meteorologic weather service) in UK https://www.metoffice.gov.uk/.

The program collects weather observations data from the TFA cloud service https://www.data199.com.
The format and API is found here; https://mobile-alerts.eu/info/public_server_api_documentation.pdf

This program just collects outdoor temp and wind metrics, but you may collect other data depending on your configuration.

The observations are reported to the Met Office cloud service. For that you have to
1) create an Met Office account(https://register.metoffice.gov.uk/WaveRegistrationClient/public/register.do?service=weatherobservations)
2) create and define your weather station site. Instructions can be found here; https://about.metservice.com/our-company/your-weather/add-your-own-weather-station/
3) 3) It's a bit unclear what interface to use when reporting observations to the MET Office service. The one that seems to work is http://wow.metoffice.gov.uk/automaticreading.
   The interface is described here; https://wow.metoffice.gov.uk/support/dataformats

   There is also another interface that allows you to report observation, however those observation reported does not seem to be connected with https://wow.metoffice.gov.uk/ information.
   If you however like to explore that interface you can find more about it at  the Met development portal https://mowowprod.portal.azure-api.net/ where you have to another account. 
   See https://mowowprod.portal.azure-api.net/documentation/how-to-obtain-a-subscription-key for futher details. 
   The REST API for uploading data to the Met Office Azure service are found here;
    https://mowowprod.portal.azure-api.net/documentation/table-of-contents

The program will load a JSON file with your specific site, device and subscription data.
the JSON syntax for this file **_auth_keys.json_** is
```json
{ "subscription_key" : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "phone_id" : "xxxxxxxxxxxx",
  "site_id" : "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx",
  "site_auth_key" : "xxxxxx" }
```