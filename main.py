'''

REPL starts after both boot.py and main.py have finished. An endless loop in boot.py or main.py prevents REPL.

TODO: license info and other application-level info here

DS18B20 Temperature Sensor - 1 wire interface

'''
global cfg
global rtc
global wdt
global client_id

import automation
import action 

from micropython import const
import micropython_sht31d
import onewire
import ds18x20
from micron_pcd8544 import micron_PCD8544
from machine import SoftSPI, SPI, I2C, UART, WDT


# Initialize the watchdog timer
wdt = WDT(timeout=int(cfg._watchdog_timeout_ms))

# 
i2c_dev_info = {
    "0x29" : "TSL2591 Light/Lux Sensor",
    "0x39" : "AS72341 10ch Spectrometer",
    "0x44" : "SHT30D Temp and Humidity Sensor",
    "0x58" : "SGP30 TVOC and eCO2 Sensor",
    "0x5f" : "HTS221 Temp and Humidity Sensor"
}

data = {}

'''


'''
async def ds18x20_loop(pin):
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    while True:
        ds.convert_temp()
        await uasyncio.sleep_ms(1000)
        for rom in roms:
            #print(ds.read_temp(rom))
            pass

'''
TODO

handle heater of SHT30D to turn on/off

'''
async def sht30d_loop(client, i2c, secondary_offset_degc = -0.471698):
  sht = micropython_sht31d.SHT31D(i2c)
  while True:
    await uasyncio.sleep_ms(1000)
    
    # Get temperature/humidity and derivatives
    rh = sht.relative_humidity
    primary_temp_degc = sht.temperature
    secondary_temp_degc = sht.temperature + secondary_offset_degc
    primary_temp_degf = primary_temp_degc * 1.8 + 32
    secondary_temp_degf = secondary_temp_degc * 1.8 + 32
    svp_pa = 610.78 * pow(math.e, (secondary_temp_degc / (secondary_temp_degc + 238.3) * 17.2694))
    vpd_kpa = (svp_pa / 1000) * (1 - (rh / 100))
    
    data['primary_temp_degf'] = primary_temp_degf
    data['secondary_temp_degf'] = secondary_temp_degf
    data['primary_temp_degc'] = primary_temp_degc
    data['secondary_temp_degc'] = secondary_temp_degc
    data['relative_humidity'] = rh
    data['vpd_kpa'] = vpd_kpa
    
    # Publish values to MQTT
    '''
    client.publish('esp32/sht30d/primary_temp_degf', str(primary_temp_degf))
    client.publish('esp32/sht30d/secondary_temp_degf', str(secondary_temp_degf))
    client.publish('esp32/sht30d/primary_temp_degc', str(primary_temp_degc))
    client.publish('esp32/sht30d/secondary_temp_degc', str(secondary_temp_degc))
    client.publish('esp32/sht30d/relative_humidity', str(rh))
    client.publish('esp32/sht30d/vpd_kpa', str(vpd_kpa))
    '''
    
    # TODO
    #
    # find a way to store this information so that the web server can access it other than MQTT

'''
TODO documentation on system_loop
'''
async def system_loop(client):
  while True:
    client.publish('esp32/sys/cpu_freq_hz', str(machine.freq()))
    client.publish('esp32/sys/raw_temperature', str(esp32.raw_temperature()))
    client.publish('esp32/sys/hall_sensor', str(esp32.hall_sensor()))
    client.publish('esp32/sys/ram_allocated_bytes', str(gc.mem_alloc()))
    client.publish('esp32/sys/ram_available_bytes', str(gc.mem_free()))
    await uasyncio.sleep_ms(1000)


'''
TODO 
make a better driver for the display - a combination of adafruit and the current implementation
want something more simple/streamlined without neededing to do a ton of extra work outside of the
driver itself
'''
async def display_loop(spi, cs_pin=22, dc_pin=23, rst_pin=21, bl_pin=5):
  
  cs = Pin(cs_pin)
  dc = Pin(dc_pin)
  rst = Pin(rst_pin)
  
  # backlight PWM
  bl = Pin(bl_pin, Pin.OUT, value=1)
  bl_pwm = machine.PWM(bl)
  bl_pwm.freq(500)

  duty_cycle = 512
  bl_pwm.duty(duty_cycle)
  
  lcd = micron_PCD8544(spi, cs, dc, rst)
  buffer = bytearray((const(0x30) // 8) * const(0x54))
  fbuf = framebuf.FrameBuffer(buffer, const(0x54), const(0x30), framebuf.MONO_VLSB)
  
  display_index = 0

  while True:
    await uasyncio.sleep_ms(1000)
    fbuf.fill(0)

    #duty_cycle = (duty_cycle + 100) % 1024
    #bl_pwm.duty(duty_cycle)
  
    if 0 <= display_index < 1:
      fbuf.text('T-{:.2f} F'.format(data['primary_temp_degf']), 0, 0, 1)
      fbuf.text('H-{:.2f} %'.format(data['relative_humidity']), 0, 20, 1)
      fbuf.text('V-{:.2f} kPa'.format(data['vpd_kpa']), 0, 40, 1)
    elif 1 <= display_index < 2:
      (year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()
      fbuf.text('Y: {0}'.format(year), 0, 0, 1)
      fbuf.text('M: {0}'.format(month), 0, 10, 1)
      fbuf.text('D: {0}'.format(day), 0, 20, 1)
      fbuf.text('{0}:{1}:{2}.{3}'.format(hours, minutes, seconds, subseconds), 0, 30, 1)
    elif 2 <= display_index < 3:
      fbuf.text('Used RAM', 0, 0, 1)
      fbuf.text('{0}'.format(gc.mem_alloc()), 0, 10, 1)
      fbuf.text('Free RAM', 0, 20, 1)
      fbuf.text('{0}'.format(gc.mem_free()), 0, 30, 1)

    lcd.text_action.run(buffer)

    display_index = (display_index + 0.2) % 3
   

'''
TODO documentation on watchdog_loop
'''
async def watchdog_loop():
  global wdt
  while True:
    wdt.feed()
    await uasyncio.sleep_ms(1000)

'''


# this can be used to duplicate the REPL and act upon it
#uos.dupterm(stream_object)


async def repl_loop():
  uart0 = UART(0, baudrate=115200, tx=1, rx=3)
  stdin = uasyncio.StreamReader(uart0)
  while True:
    msg = await stdin.readline()
    print('echo:{0}'.format(msg))
'''
    

'''
TODO documentation on automation loop
'''
async def automation_loop(automation):
  # pass in an automation object which contains the information about it
  # define a loop rate indicated by frequency_in_ms
  # at the defined rate run the check through value and hysteresis
  # if the trigger is done then run the defined action (only update value if state change)
  await automation.run()


'''
TODO documentation on main functio
'''
async def main(client, i2c, spi):
  # create automations
  #display_automation = automation(1000, )


  await uasyncio.gather(
    #sht30d_loop(client, i2c),
    #system_loop(client),
    watchdog_loop(),
    display_loop(spi),
    #ds18x20_loop(ow),
    #repl_loop(),
    #automation_loop(display_automation)
  )

print('Initializing and scanning I2C_BUS_0...')
i2c = I2C(0)
devices = i2c.scan()
for device in devices:
    id = hex(device)
    if id in i2c_dev_info:
        print('I2C Device found: ID {0} - {1}'.format(id, i2c_dev_info[id]))
    else:
        print('I2C Device found: ID {0} - {1}'.format(id, 'Unknown'))

spi_baud = 2000000
print ('Initializing SPI_BUS_1 with baudrate of {0}...'.format(spi_baud))
spi = SoftSPI(baudrate=spi_baud, polarity=0, phase=0, sck=Pin(22), mosi=Pin(21), miso=Pin(23))
spi.init(baudrate=spi_baud)

'''
print('Initializing and scanning OneWire bus...')
ow = onewire.OneWire(Pin(27))
print(ow.scan())
ow.reset()
'''

'''
client = MQTTClient(client_id, cfg.mqtt_server)
client.connect()
print('Connected to %s MQTT broker' % (cfg.mqtt_server))
'''
client = None

# setup interrupts
# button = Pin(26, Pin.IN, pull=Pin.PULL_DOWN)
# button.irq(handler=button_handler)

uasyncio.run(main(client, i2c, spi))



