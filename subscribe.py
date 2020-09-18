#!/usr/bin/python
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import time
import os
import sys
import datetime

pid=str(os.getpid())
pidfile = "subscribe.pid"

if os.path.isfile(pidfile):
    sys.exit()
open(pidfile,"w").write(pid)


thingid = os.getenv('thingid','actor')
brokeraddr = os.getenv('brokeraddr','openhabian')
pin = int(os.getenv('pin', '17'))

thingTopic = "jumajumo/" + thingid + "/"
commandTopic = thingTopic + "command"

ON=gpio.LOW
OFF=gpio.HIGH

gpio.setmode(gpio.BCM)
gpio.setup(pin,gpio.OUT)
gpio.output(pin,OFF)

def on_message(client, userdata, message):

   if message.topic == commandTopic:
      msgReceived = message.payload
      if "ON" == msgReceived.decode():
         gpio.output(pin,ON)

      if "OFF" == msgReceived.decode():
         gpio.output(pin,OFF)

def on_disconnect():
   gpio.output(pin,OFF)

client = mqtt.Client(thingid)

client.on_message=on_message
client.on_disconnect=on_disconnect

client.will_set(thingTopic + "sys/state", "OFFLINE", qos=1, retain=True)

client.connect(brokeraddr,keepalive=600)

client.publish(thingTopic + "env/thingid", thingid, qos=1, retain=True)
client.publish(thingTopic + "env/brokeraddr", brokeraddr, qos=1, retain=True)
client.publish(thingTopic + "env/pin", pin, qos=1, retain=True)

client.publish(thingTopic, str(datetime.datetime.now()), qos=1, retain=True)
client.publish(thingTopic + "sys/type", "actor", qos=1, retain=True)
client.publish(thingTopic + "sys/device", "relais-switch_on-off", qos=1, retain=True)
client.publish(thingTopic + "sys/state", "ONLINE", qos=1, retain=True)

client.publish(commandTopic, "ONLINE")

client.subscribe(commandTopic, qos=0)

try:
   client.loop_forever()
finally: 
   os.unlink(pidfile)

