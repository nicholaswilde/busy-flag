#!/usr/bin/env python3

import time
import logging
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
CHANNELS = 16

ACTUATION_RANGE = 180

CHANNEL = 0

kit = ServoKit(channels=CHANNELS)

#class Servo:
#	def __init__(self, s):

#kit.servo[SERVO_NO].actuation_range = ACTUATION_RANGE

#kit.servo[0].set_pulse_width_range(1000, 2000)

def main():
	print("test1")
	kit.servo[CHANNEL].angle = 120
	time.sleep(2)


def home():
	kit.servo[CHANNEL].angle = 0
	time.sleep(2)


if __name__ == '__main__':
	home()
	main()
	home()
