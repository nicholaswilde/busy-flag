#!/usr/bin/env python3

import time
from adafruit_servokit import ServoKit


# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
CHANNEL = 16

kit = ServoKit(channels=CHANNEL)

def main():
	kit.servo[0].angle = 180
	kit.continuous_servo[1].throttle = 1
	time.sleep(1)
	kit.continuous_servo[1].throttle = -1
	time.sleep(1)
	kit.servo[0].angle = 0
	kit.continuous_servo[1].throttle = 0

if __name__ == '__main__':
	main()
