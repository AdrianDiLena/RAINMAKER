import darksky as ds
from darksky import forecast
import time
import datetime
import paho.mqtt.client as mqtt
import statistics

key = '75de5122bd612375391c281fe3ce75cc'

broker_url = '192.168.2.67'
broker_port = 1883

rainmaker = mqtt.Client()
rainmaker.connect(broker_url, broker_port)

while True:
    parkdale = forecast(key, 43.638316, -79.440705)
    pdt = (parkdale.temperature -32)*5/9
    pdo = parkdale.ozone
    print('\n--------------------------\nPARKDALE WEATHER')
    print('Hourly Summary: ' + parkdale['minutely']['summary'])
    print('Temperature Now: ' + "%.2f" % pdt + ' Celsius')
    raintoday = [hour.precipProbability for hour in parkdale.hourly[:12]]
    print('Chance of rain: ' + str(statistics.median(raintoday)))
    #print('Chance of rain today: ' + str(parkdale['minutely']['data'][0]['precipProbability']))
    mintemptime = datetime.datetime.fromtimestamp(parkdale['daily']['data'][0]['temperatureMinTime'])
    maxtemptime = datetime.datetime.fromtimestamp(parkdale['daily']['data'][0]['temperatureMaxTime'])
    print('\nMin Temperature: ' + str((parkdale['daily']['data'][0]['temperatureMin']-32)*5/9) + ' @ ' + (mintemptime.strftime('%H:%M:%S')))
    print('Max Temperature: ' + str((parkdale['daily']['data'][0]['temperatureMax']-32)*5/9) + ' @ ' + (maxtemptime.strftime('%H:%M:%S')))
    print('\nThis Week:')
    print(parkdale.daily.summary)
    print('--------------------------')
    time.sleep(5)

    # Morning Rain Probability Check    
    if time.localtime()[3] == 8 and time.localtime()[4] == 1 and time.localtime()[5] <= 10:
        print('Checking next 12 hours for PrecipProbability in Parkdale...')
        rainHours = [hour.precipProbability for hour in parkdale.hourly[:12]]
        print(rainHours)
        rainMedian = statistics.median(rainHours)
        
        if rainMedian < 0.6:
            rainmaker.publish(topic = 'RAINMAKER/relays/valve1', payload = 'on')
            rainmaker.publish(topic = 'RAINMAKER/relays/valve2', payload = 'on')
            print('TURN ON THE FUCKING RAIN!')
        else:
            print('No water this morning... ITS GONNA RAIN!')
            break

    # Evening Rain Probability Check
    if time.localtime()[3] == 20 and time.localtime()[4] == 3 and time.localtime()[5] <= 10:
        print('Checking next 12 hours for PrecipProbability in Parkdale...')
        rainHours = [hour.precipProbability for hour in parkdale.hourly[:12]]
        print(rainHours)
        rainMedian = statistics.median(rainHours)
        print('Median Probability over next 12 hours: ' + str(rainMedian))
        if rainMedian < 0.6:
            rainmaker.publish(topic = 'RAINMAKER/relays/valve1', payload = 'on')
            rainmaker.publish(topic = 'RAINMAKER/relays/valve2', payload = 'on')
            print('TURN ON THE FUCKING RAIN!')
        else:
            print('No water this evening... ITS GONNA RAIN!')
            break
