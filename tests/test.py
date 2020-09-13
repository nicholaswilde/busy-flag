#!/usr/bin/env python3

import time
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
SPEED = 0.75

# The overall PWM frequency of the PCA9685 in Hertz. Default frequency is ``50``.
FREQUENCY = 50

# The I2C address of the PCA9685. Default address is ``0x40``.
# Can be found by running sudo i2cdetect -y 1
ADDRESS_SERVO=0x40

class Flag(ServoKit):
  def __init__(self, channels, frequency, address, channel, angle_up=120, angle_down=0, speed=1, angle_home=None):
    super().__init__(channels=channels, frequency=frequency, address=address)
    if not 0.1 <= speed <= 1.0:
      raise ValueError("Speed must be 0.1 to 1.0")
    # Assume home is the same as down
    if angle_home is None:
      angle_home = angle_down
    self.angle_home = angle_home
    self.channel = channel
    self.angle_up = angle_up
    self.angle_down = angle_down
    self.speed = speed
    self.flag = self.servo[channel]

  def up(self):
      self._move(self.angle_up)
      
  def down(self):
      self._move(self.angle_down)
		
  def home(self):
    self._move(self.angle_home, 1)

  @property
  def angle(self):
    return self.flag.angle
    
  @angle.setter
  def angle(self, value):
    self.flag.angle = value
    
  @property
  def fraction(self):
    return self.flag.fraction
  
  @fraction.setter
  def fraction(self, value):
    self.flag.fraction = value
  
  # Speed control
  def _move(self, n, s=None):
    if s is None:
      s = self.speed
    s = 430*s
    # Which direction do we need to go
    if n > self.flag.angle:
      i = 1
    else:
      i = -1
    t = round(1/s-1/450, 4)
    for angle in range(int(self.flag.angle), n, i):  # 0 - 180 degrees, 5 degrees at a time.
      self.flag.angle = angle
      time.sleep(t)

f = Flag(channels=CHANNELS, frequency=FREQUENCY, address=ADDRESS_SERVO, channel=CHANNEL_SERVO, angle_up=ANGLE_UP, angle_down=ANGLE_DOWN, speed=SPEED)

if __name__ == '__main__':
  f.home()
  print(f.angle)
  time.sleep(1)
  f.up()
  print(f.angle, f.speed)
  time.sleep(1)
  f.down()
