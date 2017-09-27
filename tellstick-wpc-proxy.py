#!/usr/bin/env python

# This script will convert WPC3 JSON from Tellstick to W, Wh and kWh.
# https://github.com/senilio/tellstick-wpc-proxy

import web
import json
import time
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

# URL to your Tellstick local API sensor
url = 'http://192.168.88.17/api/sensor/info?id=9'

# Tellstick API key
api_key = 'Bearer bloody_long_key'

# Electric meter blink factor
# blinkFactor is 1000 divided by the Electric meter parameter.
# Usually 1000 or 10000 impulses per kWh
blinkFactor = 1000.0/10000.0

# Create urllib object
req = Request(url)
req.add_header('Authorization', api_key)

# Path to execute class
commands = ('/get_wpc', 'get_wpc')
app = web.application(commands, globals())

# How often in seconds are you polling for new data?
# This is used to properly calculate momentary power usage [Watt].
poll_frequency = 12

# Init variables
prev_count = 0
prev_time = 0

# Class to handle the WPC3 data
class get_wpc:
    def GET(self):
        # Use prev_count and prev_time from global()
        global prev_count, prev_time

        # Read data from Tellstick and create JSON object
        response = urlopen(req).read().decode('utf-8')
        jsonvar = json.loads(response)

        # Set current time
        current_time = time.time()

        # Get current counter and multiplier
        current_value = jsonvar['data'][0]['value']
        multiplier = jsonvar['data'][1]['value']

        # Do the math to convert Tellstick data to real count
        if current_value >= 0.0:
            count = multiplier*4096 + 10*current_value
        else:
            count = multiplier*4096 - 10*current_value + 2048

        # Fix for messed up first poll
        if prev_count == 0:
            prev_count = count
        if prev_time == 0:
            prev_time = current_time - poll_frequency

        # Calc diff between latest and 2nd latest count
        count_diff = count - prev_count
        prev_count = count

        # Time since last poll. Used to calc momentary W.
        time_diff = current_time - prev_time

        # Check if count have overflowed
        if count_diff < 0:
            count_diff += 393216

        # Calc usage
        powerW = count_diff*blinkFactor*60.0*(60.0/time_diff)
        energykWh = count_diff*blinkFactor / 1000

        # Submit new value and rename variables
        jsonvar['data'][0]['name'] = 'powerW'
        jsonvar['data'][1]['name'] = 'energykWh'
        jsonvar['data'][0]['value'] = powerW
        jsonvar['data'][1]['value'] = energykWh

        # Set prev_time
        prev_time = current_time

        # Return modified JSON
        return json.dumps(jsonvar, indent=4, sort_keys=True)

if __name__ == "__main__":
    # Start web service
    app.run()
