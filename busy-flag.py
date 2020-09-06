#!/usr/bin/env python3

import json
import board
import busio

from time 				import sleep
from datetime 			import datetime
from gpiozero 			import CPUTemperature
from flask 				import Flask, jsonify, make_response, request, send_from_directory
from flask_cors 		import CORS
from jsmin				import jsmin
from adafruit_servokit	import ServoKit
from adafruit_pca9685	import PCA9685

globalRed = 0
globalGreen = 0
globalBlue = 0
globalBrightness = 0
globalLastCalled = None
globalLastCalledApi = None
globalStatus = None
globalStatusOverwrite = False

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
CHANNELS = 16
CHANNEL_SERVO = 0	# Channel of servo
CHANNEL_LED = 1		# Channel of LED
ANGLE_UP = 0
ANGLE_DOWN = 115
HOST = '0.0.0.0'
DEBUG = True
DUTY_CYCLE_ON = 0xffff
DUTY_CYCLE_OFF = 0

# The overall PWM frequency of the PCA9685 in Hertz. Default frequency is ``50``.
FREQUENCY = 50

# The I2C address of the PCA9685. Default address is ``0x40``.
# Can be found by running sudo i2cdetect -y 1
ADDRESS_SERVO=0x40


# LED
hat = PCA9685(busio.I2C(board.SCL, board.SDA))
led = hat.channels[CHANNEL_LED]

class Servo(ServoKit):
	def __init__(self, channels, frequency, address, channel, angle_up=0, angle_down=120):
		super().__init__(channels=channels, frequency=frequency, address=address)
		self.channel = channel
		self.angle_up = angle_up
		self.angle_down = angle_down

	def up(self):
		self.servo[self.channel].angle = self.angle_up

	def down(self):
		self.servo[self.channel].angle = self.angle_down
		
	def home(self):
		self.servo[self.channel].angle = self.angle_down


class MyFlaskApp(Flask):
	def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
		super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


s = Servo(channels=CHANNELS, frequency=FREQUENCY, address=ADDRESS_SERVO, channel=CHANNEL_SERVO, angle_up=ANGLE_UP, angle_down=ANGLE_DOWN)
app = MyFlaskApp(__name__, static_folder='frontend/build', static_url_path='/')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def led_on():
	led.duty_cycle = DUTY_CYCLE_ON


def led_off():
	led.duty_cycle = DUTY_CYCLE_OFF


def up():
	print("up")
	s.up()
	led_on()
	sleep(1)


def down():
	home()


def home():
	print("home")
	s.down()
	led_off()
	sleep(1)


def setTimestamp():
	global globalLastCalled
	globalLastCalled = datetime.now()


# API Initialization
@app.route('/', methods=['GET'])
def root():
	print(app.static_folder)
	return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/on', methods=['GET', 'POST'])
def apiOn():
	global globalStatusOverwrite, globalStatus, globalLastCalledApi
	globalStatusOverwrite = False
	globalStatus = 'on'
	globalLastCalledApi = '/api/on'
	setTimestamp()
	return make_response(jsonify({}))


@app.route('/api/off', methods=['GET', 'POST'])
def apiOff():
	global globalStatusOverwrite, globalStatus, globalLastCalledApi
	globalStatusOverwrite = False
	globalStatus = 'off'
	globalLastCalledApi = '/api/off'
	setTimestamp()
	return make_response(jsonify({}))


@app.route('/api/switch', methods=['POST'])
def apiSwitch():
	global globalStatusOverwrite, globalStatus, globalLastCalledApi

	if globalStatusOverwrite:
		return make_response(jsonify({}))

	globalLastCalledApi = '/api/switch'
	content = json.loads(jsmin(request.get_data(as_text=True)))
	red = content.get('red', None)
	green = content.get('green', None)
	blue = content.get('blue', None)
	if red is None or green is None or blue is None:
		return make_response(jsonify({'error': 'red, green and blue must be present and can\' be empty'}), 500)

	if red == 0 and green == 144 and blue == 0:
		globalStatus = 'Available'
		down()
	elif red == 255 and green == 191 and blue == 0:
		globalStatus = 'Away'
		down()
	elif red == 179 and green == 0 and blue == 0:
		globalStatus = 'Busy'
		up()
	else:
		globalStatus = None
	return make_response(jsonify())


@app.route('/api/available', methods=['GET', 'POST'])
def availableCall():
	global globalStatusOverwrite, globalStatus, globalLastCalledApi
	globalStatusOverwrite = True
	globalStatus = 'Available'
	globalLastCalledApi = '/api/available'
	setTimestamp()
	down()
	return make_response(jsonify())


@app.route('/api/busy', methods=['GET', 'POST'])
def busyCall():
	global globalStatusOverwrite, globalStatus, globalLastCalledApi
	globalStatusOverwrite = True
	globalStatus = 'Busy'
	globalLastCalledApi = '/api/busy'
	setTimestamp()
	up()
	return make_response(jsonify())


@app.route('/api/away', methods=['GET', 'POST'])
def awayCall():
	global globalStatusOverwrite, globalStatus, globalLastCalledApi
	globalStatusOverwrite = True
	globalStatus = 'Away'
	globalLastCalledApi = '/api/away'
	setTimestamp()
	down()
	return make_response(jsonify())


@app.route('/api/reset', methods=['GET', 'POST'])
def resetCall():
	global globalStatusOverwrite, globalStatus, globalLastCalledApi
	globalStatusOverwrite = False
	return make_response(jsonify())


@app.route('/api/rainbow', methods=['POST'])
def apiDisplayRainbow():
	global globalStatus, globalLastCalledApi
	globalStatus = 'rainbow'
	globalLastCalledApi = '/api/rainbow'
	data = request.get_data(as_text=True)
	content = json.loads(jsmin(request.get_data(as_text=True)))
	setTimestamp()
	return make_response(jsonify())


@app.route('/api/status', methods=['GET'])
def apiStatus():
	global globalStatusOverwrite, globalStatus, globalBlue, globalGreen, globalRed, globalBrightness, \
		globalLastCalled, globalLastCalledApi

	cpu = CPUTemperature()
	return jsonify({
		'red': globalRed, 
		'green': globalGreen,
		'blue': globalBlue,
		'brightness': globalBrightness,
		'lastCalled': globalLastCalled,
		'cpuTemp': cpu.temperature,
		'lastCalledApi': globalLastCalledApi, 
		'height': 0,
		'width': 0,
		'unicorn': None,
		'status': globalStatus,
		'statusOverwritten': globalStatusOverwrite
	})


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
	app.run(host=HOST, debug=DEBUG)
