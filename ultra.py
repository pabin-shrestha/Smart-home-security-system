#importing the necessary library
import RPi.GPIO as GPIO
import time

#setting the GPIO pin mode into BOARD or into BCM by choosing the required mode
#setting the mode into BCM mode
GPIO.setmode(GPIO.BCM)

#setting the pins numbers to the required input and output
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#setting the direction for the GPIO pins that is for GPIO(IN or OUT)
GPIO.setup(GPIO_TRiGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)


#creating the function name distance to calculate the distance from and to the object or the person)
def distance():

    #setting the trigger to high
    GPIO.output(GPIO_TRIGGER,True)

    #setting the trigger to low after 0.1 millisecond)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)

    #declaring the stop and the ending time
    StartTime = time.time()
    StopTime = time.time()

    #the Start time is being saved during the process to calculate the distance in the ending
    while GPIO.input(GPIO_ECHO)==0:
        StartTime=time.time()

    #the time of the arrival is saved which is reqired to calculate the distance in the end
    while GPIO.input(GPIO_ECHO)==1:
        StopTime= time.time()


    #the difference of the time is calculated and is stored in the TimeElapsed variable.
    TimeElapsed = StopTime-StartTime

    return distance

