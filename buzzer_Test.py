import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)

while True:
    GPIO.output(23, GPIO.LOW)
    print("Buzzer on")
    sleep(0.3)
    GPIO.output(23,GPIO.HIGH)
    print("Buzzer on")
    sleep(0.3)
