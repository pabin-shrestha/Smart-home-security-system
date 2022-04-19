#importing the required library
import RPi.GPIO as GPIO
from time import sleep

#setting the GPIO pin mode in BCM mode.
#the GPIO.setwarning is declared as false to continue the work so that it donot stop the work in between. 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#the pin number is declared in the GPIO.18 number
#the port is set into HIGH at the beginning as soon as the program runs to make the buzzer beep as soon as current passes.
GPIO.setup(16, GPIO.OUT, initial= GPIO.HIGH)

# to continue the process the while loop is used
while True:
    #cuts off the current to pass through the GPIO pin
    GPIO.output(16, GPIO.LOW)
    # print in the screen
    print("LED on")

    #the sleep is used to cut off the passing of current in the pin.
    sleep(0.3)

    #again the current is passed and the buzzer beeps
    GPIO.output(16,GPIO.HIGH)
    print("LED off")

    #sleeps for 300 millisecond or 0.3 seconds.
    sleep(0.3)