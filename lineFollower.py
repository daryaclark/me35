
# First, collect sensor data
# 
# 
# 

# function to move robot forward

# threshold predefined with regards to sensor data 
# error = data from sensor - threshold 
# turn rate = proportional gain * error
# left motor moves by drive speed + turn rate 
# right motor moves by drive speed - turn rate


import RPi.GPIO as GPIO
import time
import board
import digitalio
import adafruit_apds9960.apds9960
from adafruit_apds9960.apds9960 import APDS9960

# Initialize pins using BCM mode (GPIO pin numbers not board numbers)

yellow1 = digitalio.DigitalInOut(board.D18)
yellow1.direction = digitalio.Direction.OUTPUT
red1 = digitalio.DigitalInOut(board.D17)
red1.direction = digitalio.Direction.OUTPUT
gray1 = digitalio.DigitalInOut(board.D27)
gray1.direction = digitalio.Direction.OUTPUT
green1 = digitalio.DigitalInOut(board.D22)
green1.direction = digitalio.Direction.OUTPUT

yellow2 = digitalio.DigitalInOut(board.D0)
yellow2.direction = digitalio.Direction.OUTPUT
red2 = digitalio.DigitalInOut(board.D5)
red2.direction = digitalio.Direction.OUTPUT
gray2 = digitalio.DigitalInOut(board.D6)
gray2.direction = digitalio.Direction.OUTPUT
green2 = digitalio.DigitalInOut(board.D13)
green2.direction = digitalio.Direction.OUTPUT

i2c = board.I2C()
apds = APDS9960(i2c)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

sensor.enable_color = True
apds.enable_proximity = True

sensor.color_gain = 1
# Define direction values
cw = 1
ccw = 0

proportionalGain = 1.2

# Define the steps per revolution for the motor 
steps_rev = 200

def main():
    try:
        time.sleep(5)
        while True:
            r, g, b, c = sensor.color_data
            print('Red: {0}, Green: {1}, Blue: {2}, Clear: {3}'.format(r, g, b, c))
            
            time.sleep(2)

           
            steps = 10

            ## just for red 

            redThreshold = (77 + 67 + 64) / 77
            whiteThreshold = (99 + 113 + 126) / 126

            averagedThreshold = (redThreshold + whiteThreshold) / 2

            color = "blank"

            if (r >= 77 or r <= 87) and (g >= 67 or g <= 87) and (b >= 64 or b < 84):
                color = "red"
            elif (r >= 90 or r <= 120) and (g >= 91 or g >= 130) and (b >= 98 or b <= 170):
                color = "white"
            else:
                color = "between"

            if (color == "between"):
                moveSteps(steps, 3, 3)
                # move both forward
            elif (color == "red"):
                sensorThreshold = sensorThresholdCalc(r, g, b)
                error = sensorThreshold - averagedThreshold
                turnRate = proportionalGain * error
                turnSteps = (int(turnRate))
                steps1 = steps + abs(turnSteps)
                steps2 = steps - abs(turnSteps)
                print(steps)
                moveSteps(steps1, 3, 2)
                moveSteps(steps2, 3, 1)
                # turn robot right 
            else:
                sensorThreshold = sensorThresholdCalc(r, g, b)
                error = sensorThreshold - averagedThreshold
                turnRate = proportionalGain * error
                turnSteps = (int(turnRate))
                steps1 = steps + abs(turnSteps)
                steps2 = steps - abs(turnSteps)
                print(steps)
                moveSteps(steps2, 3, 2)
                moveSteps(steps1, 3, 1)


    except KeyboardInterrupt:
        GPIO.cleanup()


def sensorThresholdCalc(r, g, b):
    if (r >= g and r >= b):
        return ((r + g + b ) / r)
    elif (g >= r and g >= b):
        return ((r + g + b ) / g)
    else:
        return ((r + g + b) / b)

def setMotor1(current_step, delay):
# This function provides the step sequence for motor 1

    if current_step == 3:
        yellow1.value = True
        red1.value = False
        gray1.value = True
        green1.value = False
        time.sleep(delay)

    elif current_step == 2:
        yellow1.value = False
        red1.value = True
        gray1.value = True
        green1.value = False
        time.sleep(delay)

    elif current_step == 1:
        yellow1.value = False
        red1.value = True
        gray1.value = False
        green1.value = True
        time.sleep(delay)
        
    elif current_step == 0:
        yellow1.value = True
        red1.value = False
        gray1.value = False
        green1.value = True
        time.sleep(delay)

def setMotor2(current_step, delay):
# This function provides the step sequence for the second motor

    if current_step == 3:
        yellow2.value = True
        red2.value = False
        gray2.value = True
        green2.value = False
        time.sleep(delay)

    elif current_step == 2:
        yellow2.value = False
        red2.value = True
        gray2.value = True
        green2.value = False
        time.sleep(delay)

    elif current_step == 1:
        yellow2.value = False
        red2.value = True
        gray2.value = False
        green2.value = True
        time.sleep(delay)
        
    elif current_step == 0:
        yellow2.value = True
        red2.value = False
        gray2.value = False
        green2.value = True
        time.sleep(delay)

def moveSteps(input_steps, speed, motor):    
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
            setMotor1(current_step, delay)
        elif motor == 2:
            setMotor2(current_step, delay)
        else: 
            setBothEqual(current_step, delay)

# def initializeMotors():
    
def setBothEqual(current_step, delay):
    if current_step == 3:
        yellow1.value = True
        red1.value = False
        gray1.value = True
        green1.value = False
        

        yellow2.value = True
        red2.value = False
        gray2.value = False
        green2.value = True

        time.sleep(delay)

    elif current_step == 2:
        yellow1.value = False
        red1.value = True
        gray1.value = True
        green1.value = False

        yellow2.value = False
        red2.value = True
        gray2.value = False
        green2.value = True
        time.sleep(delay)

    elif current_step == 1:
        yellow1.value = False
        red1.value = True
        gray1.value = False
        green1.value = True

        yellow2.value = False
        red2.value = True
        gray2.value = True
        green2.value = False

        time.sleep(delay)
        
    elif current_step == 0:
        yellow2.value = True
        red2.value = False
        gray2.value = True
        green2.value = False

        yellow1.value = True
        red1.value = False
        gray1.value = False
        green1.value = True
        time.sleep(delay)


if __name__ == "__main__":
    main()



