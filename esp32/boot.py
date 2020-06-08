import time
from umqtt.simple import MQTTClient
import machine
import micropython
import network
import esp
import webrepl
import gc
import socket
esp.osdebug(None)
from ntptime import settime
gc.collect()

# Relevant Personal Keys
ssid = 'VIRGIN930'
password = '6AF7AD59'
client_id = '75634145312158574'
mqtt_server = '192.168.2.67'
topic_sub = b'RAINMAKER'

# Set up wifi station
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print(station.ifconfig())
webrepl.start()

settime()

print('\nWelcome to RAINMAKER')
print('\nAdrian DiLena')
print('First Run: --')
print('This Version: 5.27.2020')
print('\nAutomated/Networked Sprinkler System')
