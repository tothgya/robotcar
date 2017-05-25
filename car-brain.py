#!/usr/bin/python
import time
import BaseHTTPServer

from pyfirmata import Arduino, util

HOST_NAME = '192.168.0.27' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.

board = Arduino('/dev/ttyACM0')
pinLeftPower = board.get_pin('d:10:p')
pinLeftDirection = board.get_pin('d:12:o')
pinRightPower = board.get_pin('d:11:p')
pinRightDirection = board.get_pin('d:13:o')

pinHorn = board.get_pin('d:4:o')

speed = float(0)

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
	s.send_response(200)
	s.send_header("Content-type", "text/html")
	s.end_headers()
    def do_GET(s):
	"""Respond to a GET request."""
	global speed
	s.send_response(200)
	s.send_header("Content-type", "text/html")
	s.end_headers()
	s.wfile.write("<html><head><title>Title goes here.</title></head>")
	s.wfile.write("<body><p>This is a test.</p>")
	# If someone went to "http://something.somewhere.net/foo/bar/",
	# then s.path equals "/foo/bar/".
	s.wfile.write("<p>You accessed path: %s</p>" % s.path)
	p = s.path.split('/')
	for x in p:
	    s.wfile.write("<p>Path element: %s</p>" % x)
	if p[1] == 'accelerate':
	    speed = speed + 0.1
	    if speed < 0.9 and speed > 0:
		speed = 0.9
	    if speed < 0:
		speed = 0
	    if speed > 1:
		speed = 1
	    if speed > 0:
		pinLeftDirection.write(0)
		pinLeftPower.write(speed)
		pinRightDirection.write(0)
		pinRightPower.write(speed)
	    else:
		pinLeftDirection.write(1)
		pinLeftPower.write(-speed)
		pinRightDirection.write(1)
		pinRightPower.write(-speed)
	if p[1] == 'brake':
	    speed = speed - 0.1
	    if speed < 0 and speed > -0.9:
		speed = -0.9
	    if speed < 0.9 and speed > 0:
		speed = 0
	    if speed < -1:
		speed = -1
	    if speed > 0:
		pinLeftDirection.write(0)
		pinLeftPower.write(speed)
		pinRightDirection.write(0)
		pinRightPower.write(speed)
	    else:
		pinLeftDirection.write(1)
		pinLeftPower.write(-speed)
		pinRightDirection.write(1)
		pinRightPower.write(-speed)
	if p[1] == 'stop':
		speed = 0
		pinLeftDirection.write(0)
		pinLeftPower.write(speed)
		pinRightDirection.write(0)
		pinRightPower.write(speed)
	if p[1] == 'left':
	    if speed > 0:
		pinLeftDirection.write(0)
		pinLeftPower.write(0)
		pinRightDirection.write(0)
		pinRightPower.write(speed)
	    else:
		pinLeftDirection.write(1)
		pinLeftPower.write(0)
		pinRightDirection.write(1)
		pinRightPower.write(-speed)
	if p[1] == 'right':
	    if speed > 0:
		pinLeftDirection.write(0)
		pinLeftPower.write(speed)
		pinRightDirection.write(0)
		pinRightPower.write(0)
	    else:
		pinLeftDirection.write(1)
		pinLeftPower.write(-speed)
		pinRightDirection.write(1)
		pinRightPower.write(0)
	if p[1] == 'horn':
	    pinHorn.write(1)
	    time.sleep(1)
	    pinHorn.write(0)
	s.wfile.write("<p>Speed: %s</p>" % speed)
	s.wfile.write("</body></html>")
	

if __name__ == '__main__':
     server_class = BaseHTTPServer.HTTPServer
     httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
     print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
     try:
         httpd.serve_forever()
     except KeyboardInterrupt:
         pass
     httpd.server_close()
     print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
