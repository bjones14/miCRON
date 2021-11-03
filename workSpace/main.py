'''

REPL starts after both boot.py and main.py have finished. An endless loop in boot.py or main.py prevents REPL.

TODO: license info and other application-level info here

'''
global cfg
global client_id

import micropython_sht31d

async def sht30d_loop(client, i2c):
  sht = micropython_sht31d.SHT31D(i2c)
  while True:
    client.publish('esp32/temperature', str(sht.temperature))
    client.publish('esp32/relative_humidity', str(sht.relative_humidity))
    await uasyncio.sleep_ms(1000)
    
async def main(client, sht):
  uasyncio.create_task(sht30d_loop(client, sht))
  #await uasyncio.sleep_ms(10_000)

print('Initializing and scanning I2C bus...')

i2c = I2C(0)
print(i2c.scan())

client = MQTTClient(client_id, cfg.mqtt_server)
client.connect()
print('Connected to %s MQTT broker' % (cfg.mqtt_server))

uasyncio.run(main(client, i2c))
