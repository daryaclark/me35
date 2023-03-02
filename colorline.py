from picamera2 import Picamera2
import cv2 as cv
import numpy as np
from libcamera import controls
import time
import sys
import RPi.GPIO as GPIO
import digitalio
import board

picam2 = Picamera2()

# Initialize and configure motors
yellow1 = digitalio.DigitalInOut(board.D18)
yellow1.direction = digitalio.Direction.OUTPUT
red1 = digitalio.DigitalInOut(board.D17)
red1.direction = digitalio.Direction.OUTPUT
gray1 = digitalio.DigitalInOut(board.D27)
gray1.direction = digitalio.Direction.OUTPUT
green1 = digitalio.DigitalInOut(board.D22)
green1.direction = digitalio.Direction.OUTPUT

yellow2 = digitalio.DigitalInOut(board.D23)
yellow2.direction = digitalio.Direction.OUTPUT
red2 = digitalio.DigitalInOut(board.D24)
red2.direction = digitalio.Direction.OUTPUT
gray2 = digitalio.DigitalInOut(board.D10)
gray2.direction = digitalio.Direction.OUTPUT
green2 = digitalio.DigitalInOut(board.D9)
green2.direction = digitalio.Direction.OUTPUT

# Define direction values
cw = 1
ccw = 0

# Define the steps per revolution for the motor 
steps_rev = 200

# configure camera
capture_config = picam2.create_still_configuration() #automatically 4608x2592 width by height (columns by rows) pixels
picam2.configure(capture_config)
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #sets auto focus mode

picam2.start() #must start the camera before taking any images
time.sleep(0.1)

def Motor1(current_step, delay):
# This function provides the step sequence

    if current_step == 0:
        yellow1.value = True
        red1.value = False
        gray1.value = True
        green1.value = False
        time.sleep(delay)

    elif current_step == 1:
        yellow1.value = False
        red1.value = True
        gray1.value = True
        green1.value = False
        time.sleep(delay)

    elif current_step == 2:
        yellow1.value = False
        red1.value = True
        gray1.value = False
        green1.value = True
        time.sleep(delay)
        
    elif current_step == 3:
        yellow1.value = True
        red1.value = False
        gray1.value = False
        green1.value = True
        time.sleep(delay)

def Motor2(current_step, delay):
    if current_step == 0:
        yellow2.value = True
        red2.value = False
        gray2.value = True
        green2.value = False
        time.sleep(delay)

    elif current_step == 1:
        yellow2.value = False
        red2.value = True
        gray2.value = True
        green2.value = False
        time.sleep(delay)

    elif current_step == 2:
        yellow2.value = False
        red2.value = True
        gray2.value = False
        green2.value = True
        time.sleep(delay)
        
    elif current_step == 3:
        yellow2.value = True
        red2.value = False
        gray2.value = False
        green2.value = True
        time.sleep(delay)

def BothMotors(current_step, delay):
    if current_step == 0:
        yellow1.value = True
        red1.value = False
        gray1.value = True
        green1.value = False
        time.sleep(delay)

        yellow2.value = False
        red2.value = True
        gray2.value = False
        green2.value = True
        time.sleep(delay)

    elif current_step == 1:
        yellow1.value = False
        red1.value = True
        gray1.value = True
        green1.value = False
        time.sleep(delay)

        yellow2.value = True
        red2.value = False
        gray2.value = False
        green2.value = True
        time.sleep(delay)

    elif current_step == 2:
        yellow1.value = False
        red1.value = True
        gray1.value = False
        green1.value = True
        time.sleep(delay)

        yellow2.value = True
        red2.value = False
        gray2.value = True
        green2.value = False
        time.sleep(delay)
        
    elif current_step == 3:
        yellow1.value = True
        red1.value = False
        gray1.value = False
        green1.value = True
        time.sleep(delay)

        yellow2.value = False
        red2.value = True
        gray2.value = True
        green2.value = False
        time.sleep(delay)
        

def moveSteps(input_steps, speed):    
# This function tracks the number of steps remaining based on the step input and the loop cycles

    current_step = 0
    delay = 60/(steps_rev*speed)
    
    # Determines the direction based on sign of input_steps 
    if input_steps > 0:
        direction = ccw
    if input_steps < 0:
        direction = cw
    
    for steps_remaining in range (abs(input_steps), 0, -1):
        if direction == cw: 
            if current_step >= 0 and current_step < 3:
                current_step = current_step + 1
            elif current_step == 3:
                current_step = 0
        if direction == ccw: 
            if current_step <= 3 and current_step > 0:
                current_step = current_step - 1
            elif current_step == 0:
                current_step = 3
                
        if motor == 1:   
            Motor1(current_step, delay)
        elif motor == 2:
            Motor2(current_step, delay)
        else:
            BothMotors(current_step, delay)

    print("Stepping complete! Your motor completed " + str(abs(input_steps)) + " steps at " + str(speed)+ " revolutions per minute")


while(True):
    img_name = 'image.jpg'
    picam2.capture_file(img_name) #take image 
    img = cv.imread("image.jpg") #read image with open cv, to get the bgr value of one pixel index using print(img[row][col])
    total_pixels = img.shape #returns [2529, 4608] as the shape of the image
    #create boundary for red values as two array
    lower_blue = np.array([50,40,0]) #lower range of bgr values for blue
    upper_blue = np.array([250,180,110]) #upper range of bgr values for blue

    lower_green = np.array([0, 104, 0])
    upper_green = np.array([65, 186, 72])
    #determine if the pixel in the image has bgr values within the range
    image_mask = cv.inRange(img,lower_blue,upper_blue) #returns array of 0s & 255s, 255=white=within range, 0=black=not in range
    image_maskG = cv.inRange(img, lower_green, upper_green)

    cv.imwrite("image2.jpg", image_mask) #write the mask to a new file so that it can be viewed 
    in_range = np.count_nonzero(image_mask) #count the number of elements in the array that are not zero (in other words elements that are in the red range)
    in_rangeG = np.count_nonzero(image_maskG)

    not_in_range = total_pixels[0]*total_pixels[1] - in_range 
    not_in_rangeG = total_pixels[0]*total_pixels[1] - in_rangeG

    total = total_pixels[0]*total_pixels[1]
    percent_blue = round((in_range/total)*100)
    percent_green = round((in_rangeG/total)*100)

    print(percent_blue, "%")
    print(percent_green, "%")

    if(percent_blue <= 25):
        print('Move Left!')
        motor = 2
        steps_rev = 200
        moveSteps(200,20)

        # GPIO.cleanup()

    elif (percent_blue <= 45 and percent_blue > 25):
        print('Move Right!')
        motor = 1
        steps_rec = 200
        moveSteps(-200,20)

        # GPIO.cleanup()
    else:
        print('Following Line')
        motor = 3
        steps_rec = 200
        moveSteps(200,20)
        # Check for "q" key press to end program
    if(percent_green <= 25):
        print('Move Left!')
        motor = 2
        steps_rev = 200
        moveSteps(200,10)

        # GPIO.cleanup()

    elif (percent_green <= 45 and percent_green > 25):
        print('Move Right!')
        motor = 1
        steps_rec = 200
        moveSteps(-200,10)

        # GPIO.cleanup()
    else:
        print('Following Line')
        motor = 3
        steps_rec = 200
        moveSteps(200,10)
        # Check for "q" key press to end program
    if (cv.waitKey(1) & 0xFF == ord('q')) or ():
        picam2.stop() #stop the picam    
        GPIO.cleanup()
