#!/usr/bin/env python3

import json
import constants  as c

from jsmin        import jsmin
from time         import sleep
from status       import Status
from myFlaskApp   import MyFlaskApp
from flag         import Flag

from flask        import Flask, jsonify, make_response, request, send_from_directory
from flask_cors   import CORS

import board
import busio
import adafruit_pca9685

#----------------------
# Object Declarations |
#----------------------

status = Status()

app = MyFlaskApp(__name__, static_folder='../frontend/build', static_url_path='/')

f = Flag(channels=c.CHANNELS, frequency=c.FREQUENCY, address=c.ADDRESS_SERVO,
          channel=c.CHANNEL_SERVO, angle_up=c.ANGLE_UP, angle_down=c.ANGLE_DOWN,
          speed=c.SPEED)

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = c.FREQUENCY
led_channel = hat.channels[c.CHANNEL_LED]


#------------------
# Servo API Calls |
#------------------

@app.route('/api/servo', methods=['GET','POST'])
def apiServo():
  status
  if status.statusOverwrite:
    return make_response(jsonify({}))
  content = json.loads(jsmin(request.get_data(as_text=True)))
  if content:
    angle = content.get('angle', None)
    speed = content.get('speed', None)
    print('current angle: ', f.angle)
    f.setAngle(angle=angle, speed=speed)
  return make_response(jsonify())
  
@app.route('/api/on', methods=['GET'])
def apiOn():
  led_channel.duty_cycle = 0
  return make_response(jsonify({}))
  
@app.route('/api/off', methods=['GET'])
def apiOff():
  led_channel.duty_cycle = 0xffff
  return make_response(jsonify({}))
  
#-----------------
# Core API calls |
#-----------------

# API Initialization
@app.route('/', methods=['GET'])
def root():
  print(app.static_folder)
  return send_from_directory(app.static_folder, 'index.html')
  
@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)
  
#-------
# Main |
#-------

if __name__ == '__main__':
  f.home()
  app.run(host=c.HOST, debug=c.DEBUG)
