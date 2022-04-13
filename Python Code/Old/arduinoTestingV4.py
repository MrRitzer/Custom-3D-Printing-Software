# arduino class that doesnt communicate with arduino
# Holds same methods for testing purposes but doesnt require serial communication
import time
import array
import struct

def set_mode(mode):
    return 0

# Sets num array
def set_num(x_cord,y_cord,z_cord):
    return 0

def write():
    return 0

def GetPrintStatus():
    return 0

def GoHome():
    return 0

# Repeatedly reads arduino to clear any extra data
def read_all():
    return 0

def clear_all():
    return 0

def close():
    return 0