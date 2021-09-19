'''

TODO: license info and other application-level info here

'''
global cfg

try:
  client = mqtt_connect_and_subscribe(cfg)
except OSError as e:
  mqtt_restart_and_reconnect(cfg)

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    mqtt_restart_and_reconnect()

