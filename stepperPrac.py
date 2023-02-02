## ME35 - Project 1: Game of Pies ##
## Teammates: Sebastian Fernandez, Tahseen Arefeen, Darya Clark
## Author: Darya Clark
## Goal: Control a stepper motor from the command line; Turn stepper motor 360
## degrees while raising a flag 90 degrees using a series of 3 gears in a gear
## train. 


import RPi.GPIO as GPIO
import time 

# declare variables for pins
pin1 = 12
pin2 = 11
pin3 = 13
pin4 = 15

def main():
    try:
        piSetup()
        counter = 0
        cont = True
        while cont:
            cmd = input('enter a command: ')
            step0()
            if cmd == "ff":
                forwardFullStep()
            if cmd == "bf":
                backwardFullStep()
            if cmd == "fh":
                forwardHalfStep()
            if cmd == "bh":
                backwardHalfStep()
            if cmd == "q":
                # reset stepper motor before ending program 
                cont = False
                step0()
                GPIO.cleanup()
    # if control C is using 
    except KeyboardInterrupt:
        GPIO.cleanup()

def forwardFullStep():
    # define full rotation as 200 individual steps
    for x in range(0, 200, 4):
        step1()
        step2()
        step3()
        step4()
        step0()

def backwardFullStep():
    for x in range(0, 200, 4):
        step4()
        step3()
        step2()
        step1()
        step0()

def forwardHalfStep():
    for x in range(0, 100, 4):
        step1()
        step2()
        step3()
        step4()
        step0()

def backwardHalfStep():
    for x in range(0, 100, 4):
        step4()
        step3()
        step2()
        step1()
        step0()

def piSetup():
    # makes pin an output 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)

def step0():
    GPIO.output(pin1,GPIO.LOW)
    GPIO.output(pin2,GPIO.LOW)
    GPIO.output(pin3,GPIO.LOW)
    GPIO.output(pin4,GPIO.LOW)
    time.sleep(0.01)

def step1():
    GPIO.output(pin1,GPIO.LOW)
    GPIO.output(pin2,GPIO.HIGH)
    GPIO.output(pin3,GPIO.LOW)
    GPIO.output(pin4,GPIO.HIGH)
    time.sleep(0.01)

def step2():
    GPIO.output(pin1,GPIO.HIGH)
    GPIO.output(pin2,GPIO.LOW)
    GPIO.output(pin3,GPIO.LOW)
    GPIO.output(pin4,GPIO.HIGH)
    time.sleep(0.01)

def step3():
    GPIO.output(pin1,GPIO.HIGH)
    GPIO.output(pin2,GPIO.LOW)
    GPIO.output(pin3,GPIO.HIGH)
    GPIO.output(pin4,GPIO.LOW)
    time.sleep(0.01)

def step4(): 
    GPIO.output(pin1,GPIO.LOW)
    GPIO.output(pin2,GPIO.HIGH)
    GPIO.output(pin3,GPIO.HIGH)
    GPIO.output(pin4,GPIO.LOW)
    time.sleep(0.01)


if __name__ == "__main__":
    main()