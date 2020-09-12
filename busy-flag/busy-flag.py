#!/usr/bin/env python3

import json
import constants  as c

from jsmin				import jsmin
from time         import sleep
from status       import Status
from myFlaskApp   import MyFlaskApp
from flag         import Flag

from flask        import Flask, jsonify, make_response, request, send_from_directory
from flask_cors   import CORS

status = Status()

app = MyFlaskApp(__name__, static_folder='../frontend/build', static_url_path='/')

f = Flag(channels=c.CHANNELS, frequency=c.FREQUENCY, address=c.ADDRESS_SERVO,
          channel=c.CHANNEL_SERVO, angle_up=c.ANGLE_UP, angle_down=c.ANGLE_DOWN,
          speed=c.SPEED)

@app.route('/api/servo', methods=['GET','POST'])
def apiServo():
  if status.statusOverwrite:
    return make_response(jsonify({}))

  angle = json.loads(jsmin(request.get_data(as_text=True)))
  print("angle", angle)
  if angle:
    f.angle = angle
  return make_response(jsonify())
  
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
	
if __name__ == '__main__':
  f.home()
  app.run(host=c.HOST, debug=c.DEBUG)
