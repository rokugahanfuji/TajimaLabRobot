#!/usr/bin/env python
import pygame
import time
import RPi.GPIO as GPIO
import os
import commands
import subprocess

GPIO.setmode(GPIO.BOARD)

DEVICE_ID = ""

if DEVICE_ID == "":
    print "DEVICE_ID is not set! Set the DEVICE_ID in SwitchRobot.py"
    exit()

# Initialise the pygame library
pygame.init()

# Connect to the first Joystick
print "Searching {0}...".format(DEVICE_ID)
while True:
    pygame.joystick.quit()
    pygame.joystick.init()
    if not pygame.joystick.get_count() > 0:
        subprocess.call("bluetoothctl <<< \"connect {0}\"".format(DEVICE_ID), shell=True, executable="/bin/bash")
        time.sleep(3)
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
          if event.type == pygame.JOYBUTTONUP:
            # Additional Motors
            if j.get_button(4) == False:
              C0 = False
              C1 = False
              setmotors()
            if j.get_button(5) == False:
              C0 = False
              C1 = False
              setmotors()

          if event.type == pygame.JOYBUTTONDOWN:
            # Shutdown
            if j.get_button(4) and j.get_button(5):
              c0 = False
              c1 = False
              setmotors()
              # For Joy-Con R or L
              if (j.get_button(9) and j.get_button(12)) or (j.get_button(8) and j.get_button(13)):
                GPIO.cleanup()
                subprocess.call("bluetoothctl <<< \"disconnect {0}\"".format(DEVICE_ID), shell=True, executable="/bin/bash")
		subprocess.call("sudo shutdown now", shell=True)
            # Additional Mortors
            elif j.get_button(4):
              C0 = False
              C1 = True
              setmotors()
            elif j.get_button(5):
              C0 = True
              C1 = False
              setmotors()

	  # HAT BUTTON
          if event.type == pygame.JOYHATMOTION:
              x, y = j.get_hat(0)
              input_hat = (x, y)
              # Default
              if input_hat == (0, 0):
                  A0 = False
                  A1 = False
                  B0 = False
                  B1 = False
                  setmotors()
              # Forward
              elif input_hat == (0, 1):
                  A0 = False
                  A1 = True
                  B0 = True
                  B1 = False
                  setmotors()
              # Backward
              elif input_hat == (0, -1):
                  A0 = True
                  A1 = False
                  B0 = False
                  B1 = True
                  setmotors()
              # Right
              elif input_hat == (1, 0):
                  A0 = False
                  A1 = True
                  B0 = False
                  B1 = False
                  setmotors()
              # Left
              elif input_hat == (-1, 0):
                  A0 = False
                  A1 = False
                  B0 = True
                  B1 = False
                  setmotors()

except KeyboardInterrupt:
    # Turn off the motors
    GPIO.output(MotorAE, False)
    GPIO.output(MotorBE, False)
    GPIO.output(MotorCE, False)
    j.quit()#!/usr/bin/env python

GPIO.cleanup()
