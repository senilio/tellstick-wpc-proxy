# tellstick-wpc-proxy
Simple python web service that rewrites and serves the WPC3 JSON output from Tellstick API.

WPC3 is a pulse counter device made by Niclas Forslund - see http://foogadgets.tictail.com/product/wpc3

Due to limitations in the Tellstick software, we're forced to use a workaround to support large integers, which is needed for pulse counters.

Modify script to your liking, then start it in the background using with:

```python tellstick-wpc-proxy.py port &>/dev/null &```

Then get the modified data by:

```curl http://your_ip:port/get_wpc```
