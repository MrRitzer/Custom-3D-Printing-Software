import serial
import time
import array
import struct

arduino = serial.Serial(port='COM17', baudrate=9600, timeout=0.1) # CORRECT THE PORT WHEN USING A DIFFERENT MACHINE AND VERIFY THE BAUDRATE
num = array.array('i',(0 for i in range (0,6)))  # Initializes array

# Sets num array
def set_num(x_cord,y_cord,z_cord,x_dir,y_dir,z_dir):
    num[0] = x_cord
    num[1] = y_cord
    num[2] = z_cord
    num[3] = x_dir
    num[4] = y_dir
    num[5] = z_dir

# Mode needs to be set before any coordinates are sent
def set_mode(mode):
    arduino.write(struct.pack("i",mode))

def write():
    arduino.write(struct.pack("iiiiiii", 1, num[0], num[1], num[2],num[3], num[4], num[5])) # Sends array to arduino

def GetPrintStatus():
    set_mode(2)
    temp = arduino.readline().decode('ASCII')
    print(temp)

def GoHome():
    set_mode(3)
    

# Repeatedly reads arduino to clear any extra data
def read_all():
    temp = arduino.readline().decode('ASCII')
    while temp != '':
        print(temp)
        temp = arduino.readline().decode('ASCII')

def clear_all():
    temp = arduino.readline().decode('ASCII')
    while temp != '':
        temp = arduino.readline().decode('ASCII')

def close():
    arduino.close()