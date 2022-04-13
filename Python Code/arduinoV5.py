import string
import serial
import time
import array
import struct

arduino = serial.Serial(port='COM17', baudrate=9600, timeout=0.1) # CORRECT THE PORT WHEN USING A DIFFERENT MACHINE AND VERIFY THE BAUDRATE

# Mode needs to be set before any coordinates are sent
def _setMode(mode):
    mode = "<"+str(mode)+">"
    arduino.write(mode.encode())
    # numLoops = len(mode)
    # n = 0
    # while n < numLoops:
    #     tempStr = mode[n]
    #     arduino.write(tempStr.encode())

def write(x,y,z):
    msg = str(x)+","+str(y)+","+str(z)+","
    _setMode(msg)

def startPrt():
    _setMode(1)

def pausePrt():
    _setMode(2)

def stopPrt():
    _setMode(3)

def GoHome():
    _setMode(4)

def SetHome():
    _setMode(5)

def GetPrintStatus():
    _setMode(6)
    temp = arduino.readline().decode('ASCII')
    print(temp)

def mnlPrt():
    _setMode(7)

def test():
    # arduino.write('Hello World')
    read_all()

# Repeatedly reads arduino to clear any extra data
def read_all():
    temp = arduino.readline().decode('ASCII')
    while temp != '':
        print(temp)
        temp = arduino.readline().decode('ASCII')

def close():
    arduino.close()