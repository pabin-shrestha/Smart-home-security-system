# Importing modules 
import hashlib
import adafruit_fingerprint
import drivers
import time
import os
import glob
import picamera
import RPi.GPIO as GPIO
import smtplib
from time import sleep
import serial


uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
wrong_finger_Counter=0
mail_flag= False
FP_Match= False


# Importing modules for sending mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders

#set GPIO Mode
GPIO.setmode(GPIO.BCM)

servoPIN = 18
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(1) # Initialization

#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24

Buzzer=25
LED_RED= 21
LED_GREEN=16
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Buzzer, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.LOW)

GPIO.setwarnings(False) 


unauth = "nonlocal"
cnt = "nonlocal"

display = drivers.Lcd()
#mail sender receiver setup
sender = 'raspberrypitest2022@gmail.com'
password = 'raspberrypi2022'
receiver = 'nbpshrestha4@gmail.com'

DIR = './Database/'
FILE_PREFIX = 'image'
filename=''

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
camera = picamera.PiCamera()

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True

def send_mail():
    print ('Sending E-Mail...')
    display.lcd_clear()
    display.lcd_display_string("  Unauthorize ", 1) # Write line of text to first line of display
    display.lcd_display_string("     Acess  ", 2) # Write line of text to second line of display
    time.sleep(1) 
    display.lcd_clear()
    display.lcd_display_string("Sending Mail.. ", 1) # Write line of text to first line of display
    # Create the directory if not exists
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    # Find the largest ID of existing images.
    # Start new images after this ID value.
    files = sorted(glob.glob(os.path.join(DIR, FILE_PREFIX + '[0-9][0-9][0-9].jpg]')))
    count = 0
    
    if len(files) > 0:
        count=count+1
        # Grab the count from the last filename.
    filename = os.path.join(DIR, FILE_PREFIX + '%03d.jpg'% count)
    # Save image to fil
    print(filename)
    camera.capture(filename)
    
    # Sending mail
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Unauthorized Access at your Home'
    
    body = 'The attached image is the image of suspecious person at your door.'
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
    display.lcd_clear()
    display.lcd_display_string(" Mail Sent !!! ", 1) # Write line of text to first line of display
    time.sleep(2)
    print ('Mail sent')
    display.lcd_clear()
    display.lcd_display_string("  Mail Sent  ", 1) # Write line of text to first line of display
    display.lcd_display_string("   to Owner  ", 2) # Write line of text to second line of display
    time.sleep(1) 

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance

# pylint: disable=too-many-branches
def get_fingerprint_detail():
    global wrong_finger_Counter
    global FP_Match
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="", flush=True)
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="", flush=True)
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="", flush=True)
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        FP_Match=True
        print("Found fingerprint!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
            wrong_finger_Counter=wrong_finger_Counter+1;
        else:
            print("Other error")
        return False  
p.ChangeDutyCycle(0)
time.sleep(2)
while 1:
    unauth = 1
    cnt = 0
    display.lcd_clear()
    display.lcd_display_string("  Waiting for ", 1) # Write line of text to first line of display
    display.lcd_display_string("    Visitor  ", 2) # Write line of text to second line of display
    time.sleep(0.2) 
    GPIO.output(LED_RED,GPIO.HIGH)
    GPIO.output(LED_GREEN,GPIO.LOW)
    GPIO.output(Buzzer,GPIO.LOW)
    print (distance())
    while distance ()<40:
        display.lcd_clear()
        display.lcd_display_string("   SCAN YOUR", 1) # Write line of text to first line of display
        display.lcd_display_string(" FINGERPRINT ", 2) # Write line of text to second line of display
        cnt1=0
        while cnt1<=5:
            get_fingerprint_detail()
            cnt1=cnt1+1
            print (FP_Match)
        
            if FP_Match:
                print ('Opening the door')
                display.lcd_clear()
                display.lcd_display_string("USER VERIFIED", 1) # Write line of text to first line of display
                display.lcd_display_string("DOOR -OPEN", 2) # Write line of text to second line of display 
                GPIO.output(LED_RED,GPIO.LOW)
                GPIO.output(LED_GREEN,GPIO.HIGH)
                p.ChangeDutyCycle(9)
                time.sleep(5)
                p.ChangeDutyCycle(0)
                time.sleep(1)
                p.ChangeDutyCycle(6)
                time.sleep(1)
                p.ChangeDutyCycle(0)
                time.sleep(1)
                GPIO.output(LED_RED,GPIO.HIGH)
                GPIO.output(LED_GREEN,GPIO.LOW)
                FP_Match=False
                display.lcd_clear()
                display.lcd_display_string("Door -Closed", 1) # Write line of text to first line of display
                display.lcd_display_string(">>>>>>>>>>>>", 2) # Write line of text to second line of display
                time.sleep(2)
                wrong_finger_Counter=0;
    
            elif wrong_finger_Counter>=3:
                print("Unauthorize user")
                display.lcd_clear()
                display.lcd_display_string("   ALERT!! ", 1) # Write line of text to first line of display
                display.lcd_display_string("UNAUTHORIZED USER", 2) # Write line of text to second line of display 
                time.sleep(1)
                cnt=0
                while cnt<5:
                    GPIO.output(Buzzer, GPIO.HIGH)
                    GPIO.output(LED_RED,GPIO.HIGH)
                    time.sleep(0.2)
                    GPIO.output(Buzzer, GPIO.LOW)
                    GPIO.output(LED_RED,GPIO.LOW)
                    time.sleep(0.2)
                    cnt=cnt+1
                send_mail()
                wrong_finger_Counter=0;
            

            
        
 
   