# TFA_MetOffice

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

The program will load a JSON file with your specific site, device and subscription data.
the JSON syntax for this file **_auth_keys.json_** is
```json
{ "subscription_key" : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "phone_id" : "xxxxxxxxxxxx",
  "site_id" : "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx",
  "site_auth_key" : "xxxxxx" }
```