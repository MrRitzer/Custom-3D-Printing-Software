# If not already installed, install using 'pip install pyserial'
import serial

# Creates a variable called arduino with all the necessary serial information for the specific computer
# CORRECT THE PORT WHEN USING A DIFFERENT MACHINE AND VERIFY THE BAUDRATE
arduino = serial.Serial(port='COM17', baudrate=9600, timeout=0.1) 

# Mode needs to be set before any coordinates are sent
# Inner _setMode method is used to send mode whereas specific methods
# are used to make interface program more clear as to what they are doing
# Additionally, each number of mode is 'arbitrary' and corresponds to the
# arduino program that is running on the connected arduino

def _setMode(mode):
    mode = "<"+str(mode)+">"
    arduino.write(mode.encode())

# write is used for manually sending coordinates and works by putting
# the given x, y, z, into a format that the arduino is looking to get
# coordinates in
def write(x,y,z):
    msg = str(x)+","+str(y)+","+str(z)+","
    _setMode(msg)

########
######## Begin
########


# For each of the seven methods below their names match the button that calls
# them in the GUI. Each uses the internal _setMode and exist just to make the
# interface program more clear in it's functionality

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


########
######## End
########

# Should be called whenever the program ends, this ends serial communication
# with the arduino and is done to avoid accidentally attempting two instances
# of communication by always closing the port when the program ends.

def close():
    arduino.close()


# calls read all, isn't necessary but used in conjunction with 'Test' button
# in GUI

def test():
    _read_all()

# Repeatedly reads arduino to clear any extra data, testing method
# that is helpful when debugging additional functionality

def _read_all():
    temp = arduino.readline().decode('ASCII')
    while temp != '':
        print(temp)
        temp = arduino.readline().decode('ASCII')