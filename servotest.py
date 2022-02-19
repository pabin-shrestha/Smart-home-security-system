import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
motor = GPIO.PWM(11,40)
print("opening the door lock/ unlocking the door.")

motor.start(2)

# time.sleep(2)
motor.ChangeDutyCycle(2)
time.sleep(3)
motor.ChangeDutyCycle(10)
time.sleep(3)

print("closing door")
motor.ChangeDutyCycle(10)
time.sleep(3)
motor.ChangeDutyCycle(0)

motor.stop()


GPIO.cleanup()

