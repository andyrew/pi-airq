import requests
import json


class airnow:
    def __init__(self, api_key, zip_code=94611):
        self.api_key = api_key
        self.zip_code = zip_code
        self.url = 'http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode='+str(self.zip_code)+'&distance=25&API_KEY='+str(self.api_key)
        self.get_aqi

    def read(self):
        response = requests.get(self.url)
        data = response.json()
        self.aqi_pm25 = data[1]['AQI']

