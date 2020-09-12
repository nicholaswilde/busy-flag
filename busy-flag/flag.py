import time
from adafruit_servokit import ServoKit

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