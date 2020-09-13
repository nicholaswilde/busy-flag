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