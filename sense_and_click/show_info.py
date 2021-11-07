"""
Create the Flask application with default route and “/check-movement” route.
Read the log file and return the number of new photos since the last check.
Display the file name of the latest photo, and the photo itself, when calling the URL “/check-movement”
"""

from flask import Flask
import os

CAMERA_FOLDER_PATH = "/home/pi/camera"
LOG_FILE_NAME = CAMERA_FOLDER_PATH +"/photo_log.txt"
photo_counter = 0

# initialize flask app
app = Flask(__name__, static_url_path=CAMERA_FOLDER_PATH, static_folder= CAMERA_FOLDER_PATH)

@app.route("/")
def index():
    return "Hello"

@app.route("/check-movement")
def check_movement():
    """
    whenever the movement is detected this routine must display number of
    images clicked for every motion, last image name, last image
    """
    message = ""
    line_counter = 0
    last_photo_file_name = ""
    if os.path.exists(LOG_FILE_NAME):
        with open(LOG_FILE_NAME,'r') as f:
            for line in f:
                line_counter +=1
                last_photo_file_name = line
        global photo_counter 
        difference = line_counter - photo_counter
        message = str(difference) + "photos were taken since last checked. <br>"
        message += " Last photo: " + last_photo_file_name + "<br>"
        message += " <img src = \""+last_photo_file_name+ "\">"
        photo_counter = line_counter
    else:
        message = "Nothing new"
    return message
        

app.run(host='0.0.0.0')