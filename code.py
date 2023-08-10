import time

import urllib2

import RPi.GPIO as GPIO

trig = 2

echo = 3

led1 = 17

led2 = 14

buzzer = 4

myapi="CNHNEA1BMIZA5O0W"

baseurl = "https://api.thingspeak.com/update?api_key=%s"%myapi

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(trig,GPIO.OUT)

GPIO.setup(echo,GPIO.IN)

GPIO.setup(buzzer,GPIO.OUT)

GPIO.setup(led1,GPIO.OUT)

GPIO.setup(led2,GPIO.OUT)

def read_distance():

    alert =0

    GPIO.output(trig,True)

    time.sleep(1)

    GPIO.output(trig,False)

    pulse_st=time.time()

    while GPIO.input(echo)==0:

        pulse_st= time.time()

    pulse_end=time.time()

    while GPIO.input(echo)==1:

        pulse_end=time.time()

    pulse_durat = pulse_end - pulse_st

    distance = pulse_durat*17150

    distance = round(distance,2)


    if(distance <10):

        alert=20

        GPIO.output(buzzer,True)

        GPIO.output(led2,False)

        GPIO.output(led1,False)

        print("Danger Alert")


    elif(distance>10 and distance <100):

        alert=10

        GPIO.output(buzzer,False)

        print("Red Alert")

        GPIO.output(led1,True)

        GPIO.output(led2,False)


    else:

        alert=5

        GPIO.output(buzzer,False)

        GPIO.output(led2,True)

        GPIO.output(led1,False)

        print("Normal")


    return distance,alertwhile True:

    distance,alert = read_distance()


    print(distance)

    print(alert)

    conn = urllib2.urlopen(baseurl+'&field1=%f' %(distance)

+'&field2=%f' %(alert) )

    conn.close()


    time.sleep(0.5)
