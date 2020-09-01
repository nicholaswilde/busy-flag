#!/usr/bin/env python3

import time
from adafruit_servokit import ServoKit


# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
CHANNEL = 16

#kit = ServoKit(channels=CHANNEL)

#kit.servo[0].actuation_range = 180

#kit.servo[0].set_pulse_width_range(1000, 2000)


def main():
	print("test1")
	#kit.servo[0].angle = 180
	time.sleep(1)
	print("test2")
	#kit.servo[0].angle = 0
	time.sleep(1)
	print("test3")
	#kit.servo[0].angle = 180

if __name__ == '__main__':
	main()
