import network # type: ignore
import time
import urequests # type: ignore

# Network configuration
SSID = 'Bishop Crashpad'
PASSWORD = '193201Shepard'

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
print('Network connected:', wlan.ifconfig())

calendar_url = 'http://192.168.68.68:5000/month_events'

# Make request
try:
    response = urequests.get(calendar_url)
    data = response.json()
    print(data)
    response.close()
except Exception as error:
    print("Failed to fetch:", error)