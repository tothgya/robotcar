#!/usr/bin/python
from evdev import InputDevice, ecodes, categorize, list_devices
from pyfirmata import Arduino, util
import traceback
from car import Car
from struct import *

# micro USB on Arduino UNO
arduinoDev = '/dev/ttyUSB0'
# USB B on Arduino Mega
# arduinoDev = '/dev/ttyACM0'

board = Arduino(arduinoDev)

print "Arduino ready"
car = Car()
print "Car ready"

devices = [InputDevice(fn) for fn in list_devices()]
for device in devices:
    print(device.fn, device.name, device.phys)
    if device.name == 'VR BOX':
        gamepad = device
        print 'Gamepad found'
try:
    print(gamepad.fn, gamepad.name, gamepad.phys)
except NameError:
    print 'Gamepad not found'
    sys.exit()
for event in gamepad.read_loop():
    #print categorize(event)
    #print event
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_X:
            if event.value < 100 or event.value > 150:
                print 'X '+str(event.value)+' '+str(event.code)
                car.setAllSpeed((128 - event.value) / float(128))
            else:
                # print 'X '+str(event.value)+' '+str(event.code)
                car.setAllSpeed(0)
            # back is 255
        elif event.code == ecodes.ABS_Y:
            if event.value < 100 or event.value > 150:
                print 'Y '+str(event.value)+' '+str(event.code)
                car.turn((128 - event.value) / float(12.8))
            else:
                #print 'Y '+str(event.value)+' '+str(event.code)
                car.turn(0)
            # left is 255
    if event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_NORTH:
            print 'BTN_NORTH'
            car.horn()
        elif event.code == ecodes.BTN_SOUTH:
            print 'BTN_SOUTH'
            car.stop()
    
