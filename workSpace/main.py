'''

REPL starts after both boot.py and main.py have finished. An endless loop in boot.py or main.py prevents REPL.

TODO: license info and other application-level info here

'''
global cfg
global rtc
global wdt
global client_id

import micropython_sht31d

async def sht30d_loop(client, i2c):
  sht = micropython_sht31d.SHT31D(i2c)
  while True:
    client.publish('esp32/sht30d_temperature_degf', str(sht.temperature * 1.8 + 32))
    client.publish('esp32/sht30d_relative_humidity', str(sht.relative_humidity))
    await uasyncio.sleep_ms(1000)
    
async def system_loop(client):
  while True:
    client.publish('esp32/cpu_frequency_hz', str(machine.freq()))
    await uasyncio.sleep_ms(1000)
   
async def watchdog_loop():
  while True:
    wdt.feed()
    await uasyncio.sleep_ms(1000)
    
async def main(client, i2c):
  await uasyncio.gather(
    sht30d_loop(client, i2c),
    system_loop(client),
    watchdog_loop(),
  )
  
print('Initializing and scanning I2C bus...')

i2c = I2C(0)
print(i2c.scan())

client = MQTTClient(client_id, cfg.mqtt_server)
client.connect()
print('Connected to %s MQTT broker' % (cfg.mqtt_server))

uasyncio.run(main(client, i2c))
