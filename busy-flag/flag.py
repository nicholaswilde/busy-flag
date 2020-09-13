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
      self._move(angle=self.angle_up)
      
  def down(self):
      self._move(angle=self.angle_down)
		
  def home(self):
    self.setAngle(angle=self.angle_home, speed=1)
    
  def setAngle(self, angle, speed=None):
    if not 0.1 <= speed <= 1.0:
      raise ValueError("Speed must be 0.1 to 1.0")
    if angle is None:
      return
    if speed is None:
      speed = this.speed
    self._move(angle, speed)

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
  def _move(self, angle, speed=None):
    if speed is None:
      speed = self.speed
    speed = 430*speed
    # Which direction do we need to go
    if angle > self.flag.angle:
      i = 1
    else:
      i = -1
    t = round(1/speed-1/450, 4)
    for n in range(int(self.flag.angle), angle, i):  # 0 - 180 degrees, i degrees at a time.
      self.flag.angle = n
      time.sleep(t)