# This file is executed on every boot (including wake-boot from deepsleep)

import uasyncio
import os
import json
import config
import network
import ntptime
import math
import time
import ubinascii
import framebuf
from umqttsimple import MQTTClient
import esp
import esp32
import gc
import webrepl
import machine
from machine import Pin, I2C, RTC, WDT

_CONFIG_FILE = 'config.json'

webrepl.start()

esp.osdebug(None)
gc.collect()

with open(_CONFIG_FILE) as file: 
    file_str = file.read()
    json_dict = json.loads(file_str)
    cfg = config.config(json_dict)

client_id = ubinascii.hexlify(machine.unique_id())

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(cfg.wifi_ssid, cfg.wifi_pass)

while station.isconnected() == False:
  time.sleep(3)
  
print('Connection successful')
print(station.ifconfig())

# Synchronize real-time clock (RTC) with NTP server
rtc = RTC()
print('Synchronizing RTC with NTP server...')
print('Timezone configured as UTC{0}:00'.format(cfg._timezone_utc_offset))
print('Local time before NTP synchronization: {0}'.format(str(rtc.datetime())))
ntptime.settime()
(year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()
rtc.init((year, month, day, weekday, (hours + int(cfg._timezone_utc_offset)), minutes, seconds, subseconds)) 
print('Local time after NTP synchronization and timezone correction: {0}'.format(str(rtc.datetime())))

# Initialize the watchdog timer
wdt = WDT(timeout=int(cfg._watchdog_timeout_ms))
