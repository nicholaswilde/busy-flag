import board
import busio
from adafruit_pca9685 import PCA9685

class Led(PCA9685):
  def __init__(self, channel, i2c_bus=None, *, address=64, reference_clock_speed=25000000, frequency=60):
    if i2c_bus is None:
      i2c_bus = busio.I2C(board.SCL, board.SDA)
    super().__init__(i2c_bus=i2c_bus, address=address, reference_clock_speed=reference_clock_speed)
    super().frequency = frequency
    self.channel = channel
    