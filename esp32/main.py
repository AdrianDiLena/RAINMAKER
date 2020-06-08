import time
import machine
import urequests

led = machine.Pin(2, machine.Pin.OUT)
led.on()


"""

Simple relay control via umqtt

"""

