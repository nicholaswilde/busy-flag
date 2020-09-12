#!/usr/bin/env python3

import time
import logging
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
CHANNELS = 16
CHANNEL_SERVO = 0	# Channel of servo
CHANNEL_LED = 3		# Channel of LED
ANGLE_UP = 120
ANGLE_DOWN = 0
HOST = '0.0.0.0'
DEBUG = True
DUTY_CYCLE_ON = 0xffff
DUTY_CYCLE_OFF = 0

# The overall PWM frequency of the PCA9685 in Hertz. Default frequency is ``50``.
FREQUENCY = 50

# The I2C address of the PCA9685. Default address is ``0x40``.
# Can be found by running sudo i2cdetect -y 1
ADDRESS_SERVO=0x40

#kit = ServoKit(channels=CHANNELS)

class Servo(ServoKit):
  def __init__(self, channels, frequency, address, channel, angle_up=120, angle_down=0, speed=1):
    super().__init__(channels=channels, frequency=frequency, address=address)
    if not 0.1 <= speed <= 1.0:
      raise ValueError("Speed must be 0.1 to 1.0")
    self.channel = channel
    self.angle_up = angle_up
    self.angle_down = angle_down
    self.speed = speed

  def up(self):
      self._move(self.angle_up, self.speed)
      
  def down(self):
      self._move(self.angle_down, self.speed)
		
  def home(self):
    self.servo[self.channel].angle = self.angle_down

  def _move(self,n,s):
    s = 430*s
    t = round(1/s-1/450, 4)
    for angle in range(0, n, 1):  # 0 - 180 degrees, 5 degrees at a time.
      self.servo[self.channel].angle = angle
      time.sleep(t)

s = Servo(channels=CHANNELS, frequency=FREQUENCY, address=ADDRESS_SERVO, channel=CHANNEL_SERVO, angle_up=ANGLE_UP, angle_down=ANGLE_DOWN, speed=0.1)

if __name__ == '__main__':
  s.home()
  time.sleep(1)
  s.up()
