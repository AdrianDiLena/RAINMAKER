import darksky as ds
from darksky import forecast
import time
import datetime
import paho.mqtt.client as mqtt

key = '75de5122bd612375391c281fe3ce75cc'

broker_url = '192.168.2.67'
broker_port = 1883

rainmaker = mqtt.Client()
rainmaker.connect(broker_url, broker_port)

while True:
    parkdale = forecast(key, 43.638316, -79.440705)
    pdt = (parkdale.temperature -32)*5/9
    pdo = parkdale.ozone
    print('PARKDALE WEATHER')
    print('Hourly Summary: ' + parkdale['minutely']['summary'])
    print('Today:')
    print('Temperature: ' + "%.2f" % pdt + ' Celsius')
    print('Chance of Precip: ' + str(parkdale['minutely']['data'][0]['precipProbability']))
    mintemptime = datetime.datetime.fromtimestamp(parkdale['daily']['data'][0]['temperatureMinTime'])
    maxtemptime = datetime.datetime.fromtimestamp(parkdale['daily']['data'][0]['temperatureMaxTime'])
    print('Min Temperature: ' + str((parkdale['daily']['data'][0]['temperatureMin']-32)*5/9) + ' @ ' + (mintemptime.strftime('%H:%M:%S')))
    print('Max Temperature: ' + str((parkdale['daily']['data'][0]['temperatureMax']-32)*5/9) + ' @ ' + (maxtemptime.strftime('%H:%M:%S')))
    print('Max Temp Time: ' + (maxtemptime.strftime('%H:%M:%S')))
    print('\nThis Week:')
    print(parkdale.daily.summary)
    print('--------------------------')
    
    dayrain = [0, 1, 2, 3, 4, 5, 6, 7]
    for i in dayrain[:]:
        if parkdale['daily']['data'][i]['precipProbability'] > 0.5:
            print('Chance of Rain: ' + str(parkdale['hourly']['data'][i]['precipProbability']))
            if (parkdale['hourly']['data'][i]['precipIntensity']) > 0:
                print('Rain Intensity: ' + str(parkdale['hourly']['data'][i]['precipIntensity']))
                rainmaker.publish(topic = 'SMOKESHOW/relays/light', payload = 'on')
            else:
                print('Light Rain')
    print('\nxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    
    time.sleep(3)

# There's got to be a better way to do this. 
# Manually making the list seems ugly.
