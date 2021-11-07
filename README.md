# motion-detection-with-Raspberry-Pi

movement_detector.py:

- Step1: Setup the code for the PIR sensor. Detect when there is movement. If there is movement, check that the movement has been detected for 3 full consecutive seconds. If yes, check that we didn?t take a photo in the last 60 seconds. If yes, then print a message to say we are going to take a photo and send it by email. Also, power on one LED when the PIR sensor detects movement.

- Step 2: Setup the camera before the main while loop. Create the function to take a photo and save it into a file. Call that function from the main while loop.

- Step 3: In the setup section of the program, remove the log file if it exists. Create the function to save new photo paths to the log file, and call that function just after taking a photo.

- Step 4: Setup email with Yagmail. Create the function to send an email with an attachment. Call that function just after updating the log file.

show_info.py:

- Step 5: Create the Flask application with default route and ?/check-movement? route. Read the log file and return the number of new photos since the last check.
- Step 6: Display the file name of the latest photo, and the photo itself, when calling the URL ?/check-movement?

- Step 7 (Bonus): Start the 2 Python programs on boot with systemd, so you don't need to manually get access to your Pi and start the programs from the terminal.
