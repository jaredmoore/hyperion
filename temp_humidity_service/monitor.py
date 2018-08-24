#!/usr/bin/python

# DHT Sensor Data-Logging

# Author: Jared Moore 
# Recommend reading blog article: https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
#
# Above blog contains initial code that this script has been adapted from.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import datetime
from pytz import timezone
import Adafruit_DHT

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# Example of sensor connected to Raspberry Pi
DHT_PIN  = 4 

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 600 

LOGFILE="/home/pi/logs/temp_humidity.csv"
tz = timezone('EST')

print('Logging sensor measurements to {0} every {1} seconds.'.format(LOGFILE, FREQUENCY_SECONDS))
print('Press Ctrl-C to quit.')
while True:
    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity is None or temp is None:
        time.sleep(2)
        continue

    print(datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'))
    print('Temperature: {0:0.1f} C'.format(temp))
    print('Humidity:    {0:0.1f} %'.format(humidity))

    # Append the data in the spreadsheet, including a timestamp
    with open(LOGFILE,'a') as f:
        f.write(datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')+',')
        f.write(str(temp)+',')
        f.write(str(humidity)+"\n")

    # Wait 30 seconds before continuing
    print('Wrote a row to {0}'.format(LOGFILE))
    time.sleep(FREQUENCY_SECONDS)
