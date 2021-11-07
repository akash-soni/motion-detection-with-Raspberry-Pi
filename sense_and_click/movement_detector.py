"""
Detect when there is movement.
If there ismovement, check that the movement has been detected for 3 full consecutive seconds.
If yes, check that we didn’t take a photo in the last 60 seconds.
If yes, then print a message to say we are going to take a photo and send it by email.
Also, power on one LED when the PIR sensor detects movement.
Maintain logs
"""

import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os
import yagmail

def take_photo(camera):
    """
    descripiton : function which can take pictures
    output: saves image to specified directory
    """
    # file name along with time stamp
    file_name = "/home/pi/camera/img_"+str(time.time()) + ".jpg" 
    camera.capture(file_name)
    return file_name

def update_log_file(text_line):
    # open file in append mode
    with open(LOG_FILE_NAME, "a") as f:
        f.write(str(time.time()) + " : " + text_line)
        f.write("\n")

def update_photo_log_file(line):
    # open file in append mode
    with open(LOG_IMAGE_NAME, "a") as f:
        f.write(line)
        f.write("\n")

def send_email_with_photo(yagmail_client, file_name):
    """
    The function setups the email client and description
    input : image clicked by rapberry pi camera
    output : email with image as attachemnt
    
    """
    yagmail_client.send(to = "akash.200287@gmail.com",
                        subject = "movement detected !",
                        contents = "Here's a photo taken by raspberry Pi",
                        attachments = file_name)
                          

PIR_PIN = 4 # PIR Sensor Pin attached at 4th GPIO pin
LED_PIN = 17 # Led attached with 17th GPIO pi
LOG_FILE_NAME = "/home/pi/sense_and_click/log_file.txt" # log file for maintaining text logs
LOG_IMAGE_NAME = "/home/pi/camera/photo_log.txt" # log file for maintaining text logs

# Remove log file
if os.path.exists(LOG_FILE_NAME):
    os.remove(LOG_FILE_NAME)
    print("Log file removed")

# setup camera
camera = PiCamera()
camera.resolution = (720,480)
camera.rotation = 180
print("waiting 2 seconds to initialize the camera..")
update_log_file("waiting 2 seconds to initialize the camera..")
time.sleep(2)
print("camera setup complete")
update_log_file("camera setup complete")


# setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN) # setup up PIR as input device
GPIO.setup(LED_PIN, GPIO.OUT) # setup LED pin to indicate motion detected
GPIO.output(LED_PIN, GPIO.LOW) # initially led will be off
print("GPIO setup complete")
update_log_file("GPIO setup complete")

# setup yagmail
password = ""
with open("/home/pi/.local/share/.email_password", "r") as f:
    password = f.read()
yag = yagmail.SMTP("iakashsoni20@gmail.com", password)
print("Email setup complete")
update_log_file("Email setup complete")

print("all setup complete")
update_log_file("all setup complete")

MOV_DETECT_THRESHOLD = 3.0 # time duration for detection
last_pir_state = GPIO.input(PIR_PIN) # get the present status of PIR
movement_timer = time.time() # initialize seconds timer
MIN_DURATION_BETWEEN_2_PHOTOS = 60.0 # 
last_time_photo_taken = 0
try:
    while True:
        time.sleep(0.01)
        pir_state = GPIO.input(PIR_PIN) # capture the PIR input
        
        # if motion is detected turn on LED
        if pir_state == GPIO.HIGH:
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            
        #check if last state is low and current it changed to high the start recording time
        if last_pir_state == GPIO.LOW and pir_state == GPIO.HIGH:
            movement_timer = time.time()
            
        # last state and current state is high then check 
        # if High state exist for 3 seconds then click photo and send it via email
        if last_pir_state == GPIO.HIGH and pir_state == GPIO.HIGH:
            if time.time() - movement_timer > MOV_DETECT_THRESHOLD:
                # we need to have a gap of 60 seconds between current and the last photo
                if time.time() - last_time_photo_taken > MIN_DURATION_BETWEEN_2_PHOTOS:
                    print("take a photo and send it via email")
                    photo_name = take_photo(camera)
                    update_log_file(photo_name)
                    update_photo_log_file(photo_name)
                    send_email_with_photo(yag, photo_name)
                    update_log_file("image sent")
                    last_time_photo_taken = time.time()
        last_pir_state = pir_state
        

except KeyboardInterrupt:
    GPIO.cleanup()

