#!/usr/bin/python
"""
A simple Python script to receive messages from a client over
Bluetooth using PyBluez (with Python 2).
"""
from pyfirmata import Arduino, util
import bluetooth
import traceback
from car import Car
from struct import *

# micro USB on Arduino UNO
arduinoDev = '/dev/ttyUSB0'
# USB B on Arduino Mega
# arduinoDev = '/dev/ttyACM0'

board = Arduino(arduinoDev)

maxVoltage = 7.2
minVoltage = 3.0
increment = 0.1
print "Arduino ready"
car = Car()
print "Car ready"

hostMACAddress = 'B8:27:EB:B1:34:4A'  # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
print "Bluetooth ready, wainting for connections"
s.listen(backlog)
# uuid = "34B1CF4D-1069-4AD6-89B6-E161D79BE4D8" # Windows 10 example app
uuid = "fa87c0d0-afac-11de-8a39-0800200c9a66"  # Android secure example app

bluetooth.advertise_service(s, "SampleServer",
                  service_id=uuid,
                  service_classes=[ uuid, bluetooth.SERIAL_PORT_CLASS ],
                  profiles=[ bluetooth.SERIAL_PORT_PROFILE ],
                  )
clientConnected = False
try:
    while 1:
        client, clientInfo = s.accept()
        clientConnected = True
        print "client connected"
        try:
            while clientConnected:
                print "Waiting for data"
                data = client.recv(size)
                if data:
                    print(data)
                    client.send(data)  # Echo back to client
                    # msgSize = unpack(">L", data[:4])[0]
                    p = data.split(' ')
                    # p = data[4:].split(' ')
                    # print(msgSize)
                    if p[0] == 'accelerate':
                        car.accelerate()
                    if p[0] == 'brake':
                        car.brake()
                    if p[0] == 'stop':
                        car.stop()
                    if p[0] == 'horn':
                        car.horn()
                    if p[0] == 'turn':
                        turnSpeed = 0
                        if  p[1] != 'undefined':
                            turnSpeed = int(p[1])
                        car.turn(turnSpeed)
    
        except IOError, btE:
            print "Disconnected"
            client.close()
            clientConnected = False
            print "client disconnected"
            car.stop()
            pass
except Exception, e:
    traceback.print_exc()
    print e.__class__.__name__
    print("Closing socket")
    client.close()
    s.close()
