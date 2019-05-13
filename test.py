import time

import json
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from Adafruit_IO import Client, Feed, Data, RequestError

import PMS5003
import airnow


#get key stored separately for secrecy.
with open('aio_config.json') as jsonfile:
    aio_config = json.load(jsonfile)
ADAFRUIT_IO_KEY = aio_config["aio_key"]
ADAFRUIT_IO_USERNAME = aio_config["aio_username"]

with open('airnow_config.json') as jsonfile:
    airnow_config = json.load(jsonfile)
AIRNOW_KEY = airnow_config["key"]

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
try:
    PM25 = aio.feeds('pm2-dot-5')
except RequestError:
    feed1 = Feed(name="pm2-dot-5")
    PM25 = aio.create_feed(feed1)

try:
    AQI25 = aio.feeds('aqi-pm2-dot-5')
except RequestError:
    feed2 = Feed(name="aqi-pm2-dot-5")
    PM25 = aio.create_feed(feed2)

try:
    AQI_outside = aio.feeds('aqi-outside')
except RequestError:
    feed3 = Feed(name="aqi-outside")
    AQI_outside = aio.create_feed(feed3)

# Create instance of PMS5003 object
aq_sensor = PMS5003.PMS5003(serial_terminal="/dev/serial0") 

# Create instance of airnow object
airnow_api = airnow.airnow(api_key=AIRNOW_KEY) 


# Function for cron scheduler
def post_data():
    aq_sensor.read()
    aio.append(PM25.key, aq_sensor.pm25_standard)
    aio.append(AQI25.key ,aq_sensor.aqi_pm25)
    airnow_api.read()
    aio.append(AQI_outside.key, airnow_api.aqi_pm25)

post_data()
print(aq_sensor.pm25_standard,aq_sensor.aqi_pm25, airnow_api.aqi_pm25)
