# arduino class that doesnt communicate with arduino
# Holds same methods for testing purposes but doesnt require serial communication
import time
import array
import struct

arduino = 'Object'
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

# Dummy write_read function
def write_read():
    return num[2] + 1


# Dummy read function
def read():
    return num[2] + 3

# dummy manual_write function
def manual_write():
    num = 0

# dummy clear_data function
def clear_data():
    num = 0

# dummy close function
def close():
    num = 0