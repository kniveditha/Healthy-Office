import os
import RPi.GPIO as GPIO
import time
import subprocess
import datetime

#Object declaration for getting current date and time
current = datetime.datetime.now()

#Alert  
Rasptrigger = 21

#Limitation defined according to the distance
threshold = 24

#Ultrasonic sensor 1
TRIG1 = 9
ECHO1 = 11

#Ultrasonic sensor 2
TRIG2 = 4
ECHO2 = 5

GPIO.setmode(GPIO.BCM)
#Sensor 1 setup
GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)

#Sensor 2 setup
GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.setup(Rasptrigger, GPIO.OUT)

#Global variable declaration for sonar function
pulse_start = 0
pulse_end = 0

#Function to fetch precise distance of obstacle
def sonar(trigger, echo):
	global pulse_start,pulse_end
	#Small pulse transmitter from trigger
	GPIO.output(trigger, False)
	time.sleep(1)
	GPIO.output(trigger, True)
	time.sleep(1)
	GPIO.output(trigger, False)
	
	#Small pulse receiver on echo pin
	while GPIO.input(echo)==0:
	  pulse_start = time.time()
	while GPIO.input(echo)==1:
	  pulse_end = time.time()
	
	#Difference between transmission and reception of pulse
	pulse_duration = pulse_end - pulse_start
	#Formulate time into distance
	distance = pulse_duration * 171500
	#Round the distance into readable format in cm
	distance = round(distance, 2)
	
	return distance

try:
	while True:
		distance1 = sonar(TRIG1, ECHO1)
		distance2 = sonar(TRIG2, ECHO2)
		print "Distance1:",distance1,"cm " + "Distance2:",distance2,"cm"
		if (distance1 > threshold) and (distance2 > threshold):
			#Print the datetime of leaving the table
			print "You just took a break at " + current.strftime("%Y-%m-%d %H:%M") + " good for health"
			GPIO.output(Rasptrigger, True)
			time.sleep(1)
		else:		
			GPIO.output(Rasptrigger, False)
			time.sleep(1)
except:	
	#Print on getting ctrl+c command for safe termination of program
	print "Thank you have a nice day. Created by 4Bits."

finally:
	#Safe termination and clear the state of GPIO 
	GPIO.cleanup()
