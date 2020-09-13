from led import Led
import board
import busio
import adafruit_pca9685

l = Led(channel=3)

i2c = busio.I2C(board.SCL, board.SDA)
#hat = adafruit_pca9685.PCA9685(i2c)
l.frequency = 60
#hat.frequency = 60
#led_channel = hat.channels[3]
led_channel = l.channels[3]

#led_channel.duty_cycle = 0xffff
led_channel.duty_cycle = 0

#l.channels[3].duty_cycle = 0xffff
# l.channels[3].duty_cycle = 0