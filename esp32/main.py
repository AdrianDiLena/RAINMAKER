from umqtt.robust import MQTTClient
import dht
import machine
import utime
import webrepl

webrepl.start()

client_id = '1223445'
mqtt_server = '192.168.2.67'
topic_sub = b'RAINMAKER/relays/#'

print('\n\nRAINMAKER\nVersion Delta - 6/9/2020\nThreat Level: Midnight\n\nA Weather Sensitive Irrigation System\n')

client = MQTTClient(client_id, mqtt_server)
client.connect()

led = machine.Pin(2, machine.Pin.OUT)
valve1 = machine.Pin(12, machine.Pin.OUT) # relay 1
valve2= machine.Pin(5, machine.Pin.OUT) # relay 2 
valve3 = machine.Pin(13, machine.Pin.OUT) # relay 3 
valve4 = machine.Pin(14, machine.Pin.OUT) # relay 4 

pins = [valve1, valve2, valve3, valve4, led]
for i in pins[:]:
    i.on()

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'RAINMAKER/relays/valve_one' and msg == b'on':
        valve1.off()      
    elif topic == b'RAINMAKER/relays/valve_one' and msg == b'off':
        valve1.on()
    if topic == b'RAINMAKER/relays/valve_two' and msg == b'on':
        valve2.off()      
    elif topic == b'RAINMAKER/relays/valve_two' and msg == b'off':
        valve2.on()
    if topic == b'RAINMAKER/relays/valve_three' and msg == b'on':
        valve3.off()      
    elif topic == b'RAINMAKER/relays/valve_three' and msg == b'off':
        valve3.on()
    if topic == b'RAINMAKER/relays/valve_four' and msg == b'on':
        valve4.off()      
    elif topic == b'RAINMAKER/relays/valve_four' and msg == b'off':
        valve4.on()

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to: %s \nSubscribed to: %s' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()


