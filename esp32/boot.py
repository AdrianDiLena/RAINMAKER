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

# Set up wifi station
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print(station.ifconfig())

print('\n\nWelcome to RAINMAKER')
print('\nAdrian DiLena')
print('First Run: --')
print('This Version: 6.9.2020')
print('\nAutomated/Networked Irrigation System')

