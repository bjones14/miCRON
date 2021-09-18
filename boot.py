import json
import time
from umqttsimple import MQTTClient
import micropython_sht31d
import config
import helpers
import schedule
import ubinascii
import machine
import micropython
import network
import esp
import gc

esp.osdebug(None)
gc.collect()

# Loads the JSON configuration into a config object.
cfg = load_config()

client_id = ubinascii.hexlify(machine.unique_id())

'''
topic_sub = b'notification'
topic_pub = b'hello'

last_message = 0
message_interval = 5
counter = 0
'''

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(cfg.wifi_ssid, cfg.wifi_pass)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())