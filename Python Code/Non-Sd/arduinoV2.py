import serial
import time
import array
import struct

arduino = serial.Serial(port='COM14', baudrate=115200, timeout=0.1) # CORRECT THE PORT WHEN USING A DIFFERENT MACHINE AND VERIFY THE BAUDRATE
num = array.array('i',(0 for i in range (0,3)))  # Initializes array

# Sets num array
def set_num(x_cord,y_cord,z_cord):
    num[0] = x_cord
    num[1] = y_cord
    num[2] = z_cord

# Mode needs to be set before any coordinates are sent
def set_mode(mode):
    arduino.write(struct.pack("i",mode))

def first_write():
    set_mode(1)
    arduino.write(struct.pack("iii", num[0], num[1], num[2])) # Sends array to arduino
    start_time = time.time()
    while True:
        current_time = time.time()
        data = (arduino.readline().decode('ASCII'))     # Verifies string recieved
        passed_time = current_time - start_time
        result = num[2] + 1
        if data != '':
            print("First", data)
        if data == str(result):
            break
        elif (passed_time > 5):
            data = -15.5
            break
    return int(data)


# Initial write function to verify arduino got coordinates
def write_read(x):
    set_mode(x)
    arduino.write(struct.pack("iii", num[0], num[1], num[2])) # Sends array to arduino
    start_time = time.time()
    while True:
        current_time = time.time()
        data = (arduino.readline().decode('ASCII'))     # Verifies string recieved
        passed_time = current_time - start_time
        result = num[2] + 3
        if data != '':
            print("Second: ", data)
        if data == str(result):
            break
        elif (passed_time > 5):
            data = -15.5
            break
    return int(data)

# Initial write function to verify arduino got coordinates
def write():
    set_mode(0)
    arduino.write(struct.pack("iii", num[0], num[1], num[2])) # Sends array to arduino

# Repeatedly reads arduino to clear any extra data
def clear_data():
    temp = arduino.readline().decode('ASCII')
    while temp != '':
        temp = arduino.readline().decode('ASCII')

def close():
    arduino.close()