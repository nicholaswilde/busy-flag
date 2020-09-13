#!/usr/bin/env python3

import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 60
led_channel = hat.channels[3]
led_channel.duty_cycle = 0