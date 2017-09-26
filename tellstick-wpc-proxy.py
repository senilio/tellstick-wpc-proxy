#!/usr/bin/env python

# This script will convert WPC3 JSON from Tellstick to real counts.
# https://github.com/senilio/tellstick-wpc-proxy
#

import web
import json
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

# URL to your Tellstick local API sensor
url = 'http://10.99.10.10/api/sensor/info?id=9'

# Tellstick API key
api_key = 'Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Create urllib object
req = Request(url)
req.add_header('Authorization', api_key)

# Path to execute class
commands = ('/get_wpc', 'get_wpc')
app = web.application(commands, globals())

# Class to handle the WPC3 data
class get_wpc:
    def GET(self):
        # Read data from Tellstick and create JSON object
        response = urlopen(req).read().decode('utf-8')
        jsonvar = json.loads(response)

        # Get current counter and multiplier
        current_value = jsonvar['data'][0]['value']
        multiplier = jsonvar['data'][1]['value']

        # Do the math to convert Tellstick data to real count
        if current_value >= 0.0:
            counts = multiplier*4096 + 10*current_value
        else:
            counts = multiplier*4096 - 10*current_value + 2048

        # Submit new value and rename variables
        jsonvar['data'][0]['name'] = 'blinks'
        jsonvar['data'][1]['name'] = 'multiplier'
        jsonvar['data'][0]['value'] = counts

        # Return modified JSON
        return json.dumps(jsonvar, indent=4, sort_keys=True)

if __name__ == "__main__":
    # Start web service
    app.run()
