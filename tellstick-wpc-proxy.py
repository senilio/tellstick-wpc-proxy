#!/usr/bin/env python
import web
import json
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request

# URL to your Tellstick local API sensor
url = 'http://10.99.10.10/api/sensor/info?id=9'
# API key
api_key = 'Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

req = Request(url)
req.add_header('Authorization', api_key)

commands = ('/get_wpc', 'get_wpc')
app = web.application(commands, globals())

class get_wpc:
    def GET(self):
        response = urlopen(req).read().decode('utf-8')
        jsonvar = json.loads(response)

        current_value = jsonvar['data'][0]['value']
        multiplier = jsonvar['data'][1]['value']

        if current_value >= 0.0:
            counts = multiplier*4096 + 10*current_value
        else:
            counts = multiplier*4096 - 10*current_value + 2048

        # Submit new value and return modified JSON
        jsonvar['data'][0]['name'] = 'blinks'
        jsonvar['data'][0]['value'] = counts
        return jsonvar

if __name__ == "__main__":
    app.run()
