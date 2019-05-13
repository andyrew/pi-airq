import time
time.sleep(30)

import json
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from Adafruit_IO import Client, Feed, Data, RequestError

import PMS5003


#get key stored separately for secrecy.
with open('aio_config.json') as jsonfile:
    aio_config = json.load(jsonfile)

ADAFRUIT_IO_KEY = aio_config["aio_key"]
ADAFRUIT_IO_USERNAME = aio_config["aio_username"]

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
try:
    PM25 = aio.feeds('pm2-dot-5')
except RequestError:
    feed = Feed(name="pm2-dot-5")
    PM25 = aio.create_feed(feed)

try:
    AQI25 = aio.feeds('aqi-pm2-dot-5')
except RequestError:
    feed = Feed(name="aqi-pm2-dot-5")
    PM25 = aio.create_feed(feed)

# Create instance of PMS5003 object
aq_sensor = PMS5003.PMS5003(serial_terminal="/dev/serial0") 


# Function for cron scheduler
def post_data():
    aq_sensor.read()
    aio.append(PM25.key, aq_sensor.pm25_standard)
    aio.append(AQI25.key ,aq_sensor.aqi_pm25)


# Cron like python scheduler
sched = BlockingScheduler()
sched.add_job(post_data,'cron',year='*',month='*',day='*',week='*',day_of_week='*',hour='*', minute='0/5', second='0')
sched.start()
