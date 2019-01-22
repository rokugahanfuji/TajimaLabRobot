#!/usr/bin/env python

import pygame
import time
import RPi.GPIO as GPIO
import os
import commands


GPIO.setmode(GPIO.BOARD)

joystick_name = "Joy-Con (R)"

# Initialise the pygame library
pygame.init()

# Connect to the first Joystick
print "Searching {0}...".format(joystick_name)
while True:
    pygame.joystick.quit()
    pygame.joystick.init()
    if not pygame.joystick.get_count() > 0:
        time.sleep(1)
        commands.getoutput("sh /home/pi/connect_joycon.sh")
        time.sleep(1)
        continue
    break

j = pygame.joystick.Joystick(0)
j.init()
print "Controller Detected. {0}".format(j.get_name())

# Setup the various GPIO values, using the BCM numbers for now
MotorA0 = 16
MotorA1 = 18
MotorAE = 22

MotorB0 = 23
MotorB1 = 21
MotorBE = 19

MotorC0 = 11
MotorC1 = 13
MotorCE = 15

A0 = False
A1 = False
B0 = False
B1 = False
C0 = False
C1 = False



GPIO.setup(MotorA0,GPIO.OUT)
GPIO.setup(MotorA1,GPIO.OUT)
GPIO.setup(MotorAE,GPIO.OUT)

GPIO.setup(MotorB0,GPIO.OUT)
GPIO.setup(MotorB1,GPIO.OUT)
GPIO.setup(MotorBE,GPIO.OUT)

GPIO.setup(MotorC0,GPIO.OUT)
GPIO.setup(MotorC1,GPIO.OUT)
GPIO.setup(MotorCE,GPIO.OUT)

# Set all the Motors to 'off'
GPIO.output(MotorA0, A0)
GPIO.output(MotorA1, A1)
GPIO.output(MotorAE, False)
GPIO.output(MotorBE, False)
GPIO.output(MotorB0, B0)
GPIO.output(MotorB1, B1)
GPIO.output(MotorCE, False)
GPIO.output(MotorC0, C0)
GPIO.output(MotorC1, C1)


# Only start the motors when the inputs go above the following threshold
threshold = 0.60


LeftTrack = 0
middleTrack = 0
RightTrack = 0

# Configure the motors to match the current settings.

def setmotors():
        GPIO.output(MotorA0, A0)
        GPIO.output(MotorA1, A1)
        GPIO.output(MotorAE, True)
        GPIO.output(MotorBE, True)
        GPIO.output(MotorB0, B0)
        GPIO.output(MotorB1, B1)
        GPIO.output(MotorCE, True)
        GPIO.output(MotorC0, C0)
        GPIO.output(MotorC1, C1)

# Try and run the main code, and in case of failureF we can stop the motors
try:
    # Turn on the motors
    GPIO.output(MotorAE, True)
    GPIO.output(MotorBE, True)
    GPIO.output(MotorCE, True)

    # This is the main loop
    while True:
        # Check for any queued events and then process each one
        events = pygame.event.get()
        for event in events:
          UpdateMotors = 0

          # Check if one of the joysticks has moved
          if event.type == pygame.JOYAXISMOTION:  
            if event.axis == 1:
              LeftTrack = event.value
              UpdateMotors = 1
            elif event.axis == 3:
              RightTrack = event.value
              UpdateMotors = 1
                  
            # Check if we need to update what the motors are doing
            if UpdateMotors:

              # Check how to configure the left motor

              # Move forwards
              if (RightTrack > threshold):
                  A0 = False
                  A1 = True
              # Move backwards
              elif (RightTrack < -threshold):
                  A0 = True
                  A1 = False
              # Stopping
              else:
                  A0 = False
                  A1 = False

              # And do the same for the right motor
              if (LeftTrack > threshold):
                  B0 = True
                  B1 = False
              # Move backwards
              elif (LeftTrack < -threshold):
                  B0 = False
                  B1 = True
              # Otherwise stop
              else:
                  B0 = False
                  B1 = False
            
              setmotors()
              
              
          if event.type == pygame.JOYBUTTONUP:
            if j.get_button(4) == False:
              UpdateMotors = 0
              C0 = False
              C1 = False
              setmotors()
            if j.get_button(5) == False:
              UpdateMotors = 0
              C0 = False
              C1 = False
              setmotors()
              
          if event.type == pygame.JOYBUTTONDOWN:
            if j.get_button(0) and j.get_button(3) and j.get_button(14):
                os.system('sudo shutdown now')
                time.sleep(5)
            if j.get_button(4):
              UpdateMotors = 1     
              C0 = False
              C1 = True
              setmotors()
            if j.get_button(5):
              UpdateMotors = 1     
              C0 = True
              C1 = False
              setmotors()

          if event.type == pygame.JOYHATMOTION:
              x, y = j.get_hat(0)
              input_hat = (x, y)
              # Forward
              if input_hat == (0, 1):
                  A0 = False
                  A1 = True
                  B0 = True
                  B1 = False
                  setmotors()
              # Backward
              if input_hat == (0, -1):
                  A0 = True
                  A1 = False
                  B0 = False
                  B1 = True
                  setmotors()
              # Right
              if input_hat == (1, 0):
                  A0 = False
                  A1 = True
                  B0 = False
                  B1 = False
                  setmotors()
              # Left
              if input_hat == (-1, 0):
                  A0 = False
                  A1 = False
                  B0 = True
                  B1 = False
                  setmotors()
              if input_hat == (0, 0):
                  A0 = False
                  A1 = False
                  B0 = False
                  B1 = False
                  setmotors()





except KeyboardInterrupt:
    # Turn off the motors
    GPIO.output(MotorAE, False)
    GPIO.output(MotorBE, False)
    GPIO.output(MotorCE, False)
    j.quit()#!/usr/bin/env python

GPIO.cleanup()
