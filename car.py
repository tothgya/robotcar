#!/usr/bin/python
from pyfirmata import Arduino, util
import time

# micro USB on Arduino UNO
arduinoDev = '/dev/ttyUSB0'
# USB B on Arduino Mega
# arduinoDev = '/dev/ttyACM0'

board = Arduino(arduinoDev)

maxVoltage = 9.6
minVoltage = 3.0
increment = 0.1

class Car:
    pinLeftPower = board.get_pin('d:10:p')
    pinLeftDirection = board.get_pin('d:12:o')
    pinRightPower = board.get_pin('d:11:p')
    pinRightDirection = board.get_pin('d:13:o')
    
    pinHorn = board.get_pin('d:4:o')
    
    speed = float(0)
    
    minThrottle = minVoltage / maxVoltage

    def normalizeSpeed(self, s, direction):
        if direction == 'FORWARD':
            if s < -1:
                return -1
            if s < -self.minThrottle:
                return s
            if s < 0:
                return 0
            if s < self.minThrottle:
                return self.minThrottle
            if s < 1:
                return s
            return 1
        elif direction == 'BACKWARD':
            if s > 1:
                return 1
            if s > self.minThrottle:
                return s
            if s > 0:
                return 0
            if s > -self.minThrottle:
                return -self.minThrottle
            if s > -1:
                return s
            return -1
        else: # NEUTRAL
            if s > 1:
                return 1
            if s > self.minThrottle:
                return s
            if s > -self.minThrottle:
                return 0
            if s > -1:
                return s
            return -1
    
    def setSpeed(self, pinS, pinD, s):
        pinSValue = 0
        pinDValue = False
        if s < 0:
            pinSValue = -s
            pinDValue = True
        else:
            pinSValue = s
            pinDValue = False
        
        if pinSValue != 0 or pinDValue :
            print pinS, '=', pinSValue, '|', pinD, '=', pinDValue
        pinS.write(pinSValue)
        pinD.write(pinDValue)

    def setAllSpeed(self, s):
        self.speed = s
        self.speed = self.normalizeSpeed(self.speed, 'NEUTRAL')
        self.setSpeed(self.pinLeftPower, self.pinLeftDirection, self.speed)
        self.setSpeed(self.pinRightPower, self.pinRightDirection, self.speed)
            
    def accelerate(self):
        self.speed = self.speed + increment
        self.speed = self.normalizeSpeed(self.speed, 'FORWARD')
        self.setSpeed(self.pinLeftPower, self.pinLeftDirection, self.speed)
        self.setSpeed(self.pinRightPower, self.pinRightDirection, self.speed)

    def brake(self):
        self.speed = self.speed - increment
        self.speed = self.normalizeSpeed(self.speed, 'BACKWARD')
        self.setSpeed(self.pinLeftPower, self.pinLeftDirection, self.speed)
        self.setSpeed(self.pinRightPower, self.pinRightDirection, self.speed)
        
    def turn(self, r):
        if r != 0:
            print 'Turning: ' + str(r)
        if r > 0:
            rightSpeed = self.normalizeSpeed(self.speed - (r * increment), 'BACKWARD') 
            leftSpeed = self.normalizeSpeed(self.speed, 'FORWARD')
        if r < 0:
            leftSpeed = self.normalizeSpeed(self.speed - (-r * increment), 'BACKWARD')
            rightSpeed = self.normalizeSpeed(self.speed, 'FORWARD') 
        if r == 0:
            rightSpeed = self.normalizeSpeed(self.speed, 'NEUTRAL') 
            leftSpeed = self.normalizeSpeed(self.speed, 'NEUTRAL')
        self.setSpeed(self.pinLeftPower, self.pinLeftDirection, leftSpeed)
        self.setSpeed(self.pinRightPower, self.pinRightDirection, rightSpeed)

    def stop(self):
        self.speed = 0;
        self.setSpeed(self.pinLeftPower, self.pinLeftDirection, self.speed)
        self.setSpeed(self.pinRightPower, self.pinRightDirection, self.speed)

    def horn(self):
        self.pinHorn.write(1)
        time.sleep(0.5)
        self.pinHorn.write(0)
        

