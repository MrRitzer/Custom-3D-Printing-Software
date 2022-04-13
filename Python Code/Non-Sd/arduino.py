import serial
import time
import array
import struct

arduino = serial.Serial(port='COM14', baudrate=115200, timeout=0.1) # CORRECT THE PORT WHEN USING A DIFFERENT MACHINE AND VERIFY THE BAUDRATE
num = array.array('i',(0 for i in range (0,6)))  # Initializes array

# Sets num array
def set_num(x_cord,y_cord,z_cord,x_dir,y_dir,z_dir):
    num[0] = x_cord
    num[1] = y_cord
    num[2] = z_cord
    num[3] = x_dir
    num[4] = y_dir
    num[5] = z_dir

# Prints out num array
def get_num():
    for item in num:
        print(item)

# Initial write function to verify arduino got coordinates
def write_read():
    arduino.write(struct.pack("iiiiii", num[0], num[1], num[2], num[3], num[4], num[5])) # Sends array to arduino
    start_time = time.time()
    while True:
        current_time = time.time()
        data = (arduino.readline().decode('ASCII'))     # Verifies string recieved
        passed_time = current_time - start_time
        result = num[2] + 1
        if data == str(result):
            break
        elif (passed_time > 3):
            data = -15.5
            break
    return int(data)

# Reads value from arduino to verify print finished
def read():
    start_time = time.time()
    while True:
        current_time = time.time()
        data = (arduino.readline().decode('ASCII'))     # Verifies string recieved
        passed_time = current_time - start_time
        result = num[2] + 3
        if data == str(result):
            data = result
            break
        elif (passed_time > 3):
            data = -15.5
            break
    return int(data)

# Manually writes data to arduino, doesn't do checks to verify working
def manual_write():
    arduino.write(struct.pack("iiiiii", num[0], num[1], num[2], num[3], num[4], num[5])) # Sends array to arduino
    _clear_data()

# Repeatedly reads arduino to clear any extra data
def _clear_data():
    while arduino.readline().decode('ASCII'):
        continue

def close():
    arduino.close()