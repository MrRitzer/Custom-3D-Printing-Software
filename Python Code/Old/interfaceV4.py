import PySimpleGUI as sg
import arduinoV4 as ar
from threading import Thread
import time

image_zup = 'button_icons\\white_double_arrow_up.png'
image_zdn = 'button_icons\\white_double_arrow_down.png'
image_yup = 'button_icons\\white_arrow_up.png'
image_ydn = 'button_icons\\white_arrow_down.png'
image_xlf = 'button_icons\\white_arrow_left.png'
image_xrt = 'button_icons\\white_arrow_right.png'
image_tsp = 'button_icons\\transparent.png'

# Sets icon image size for gui
def getImg(x,y):
    return sg.Image(source=image_tsp,size=(x,y))

units = {'μm.','mm.'}

### MUST BE DEFINED BEFORE PROGRAM IS RUN IN CURRENT ITERATION###
# Steps to MM ratio for specific printer software is being used on
x_conv = 0.0125
y_conv = 0.0125
z_conv = 0.0176

x_step = 1/x_conv
y_step = 1/y_conv
z_step = 1/z_conv

# Converts MM to steps, rounds to nearest step
def manualConversion(move, dir):
    if dir == 'x':
        return round(move * x_step)
    if dir == 'y':
        return round(move * y_step)
    if dir == 'z':
        return round(move * z_step)

# Manual print method for manually controlling stepper motors
def manualPrint(move, dir, unit):
    if unit == 'μm.':
        move = move / 1000
    if dir == "x_pos":
        move = manualConversion(move,'x')
        ar.set_num(move,0,0,1,1,1)
        ar.write()
    if dir == "x_neg":
        move = manualConversion(move,'x')
        move = move * -1
        ar.set_num(move,0,0,0,1,1)
        ar.write()
    if dir == "y_pos":
        move = manualConversion(move,'y')
        ar.set_num(0,move,0,1,1,1)
        ar.write()
    if dir == "y_neg":
        move = manualConversion(move,'y')
        move = move * -1
        ar.set_num(0,move,0,1,0,1)
        ar.write()
    if dir == "z_pos":
        move = manualConversion(move,'z')
        ar.set_num(0,0,move,1,1,1)
        ar.write()
    if dir == "z_neg":
        move = manualConversion(move,'z')
        move = move * -1
        ar.set_num(0,0,move,1,1,0)
        ar.write()

def comms(x,stop):
    while commStat:
        ar.set_mode(x)
        time.sleep(0.85)

# Starts the menu with an initial print status
def printMenu():
    # Icon Size:
    x = 40
    y = 40
    
    menu = [    [sg.Text("Manual Controls"),sg.T("  "*15),sg.Text("Resin Controls")],
                [getImg(1.2*x,y),sg.B(image_size=(x,y),image_filename=image_zup,key='z_pos'),getImg(x,y)],

                [getImg(1.2*x,y),sg.B(image_size=(x,y),image_filename=image_yup,key='y_pos'),getImg(x,y),
                 getImg(1.7*x,y),sg.Slider(range=(0,20),orientation='h')],

                [sg.B(image_size=(x,y),image_filename=image_xlf,key='x_neg'),
                 sg.Input(key='-UNITVALUE-',size=(3,5),pad=(0,0)),sg.Combo(list(units),default_value='mm.', size=(4,0), key='-UNITLIST-',pad=(0,0)),
                 sg.B(image_size=(x,y),image_filename=image_xrt,key='x_pos'),
                 getImg(x,y),sg.B('Start Resin'), sg.B('Stop Resin'),sg.B('Prime Resin')],

                [getImg(1.2*x,y),sg.B(image_size=(x,y),image_filename=image_ydn,key='y_neg'),getImg(x,y)],

                [getImg(1.2*x,y),sg.B(image_size=(x,y),image_filename=image_zdn,key='z_neg'),getImg(x,y)],
                
                [getImg(x,y)],

                [sg.B('Set Home'),sg.B('To Home'),sg.B('Get Status'),sg.B('Read Printer')],

                [sg.B('Start/Resume Print'), sg.B('Pause Print'), sg.B('Stop Print'), sg.B('Quit')]
                
                 ]

    # Create the window 
    window = sg.Window('Printer Interface', menu)


    printThread = Thread()
    global commStat

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            try:
                commStat = False
                printThread.join()
                ar.close()
                break
            except:
                ar.close()
                break
        # Program works on this side, needs more testing on arduino side
        # Auto Print Needs Printer Working to Test
        if event == 'Start/Resume Print':
            ar.set_mode(4) #Good
            commStat = True
            printThread = Thread(target=comms, args=(4,lambda: commStat,))
            printThread.start()
        
        if event == 'Pause Print':
            commStat = False
            printThread.join()
            ar.set_mode(13) #Good
        
        if event == 'Stop Print':
            try:
                commStat = False
                printThread.join()
                ar.set_mode(6)  #Good
            except:
                print("RuntimeError: cannot join thread before it is started")
        
        if event == 'Set Home':
            ar.set_mode(5) #Good

        if event == 'To Home':
            ar.set_mode(3) #Good
            
        if event == 'Read Printer':
            ar.read_all() #Good

        if event == 'Get Status':
            ar.GetPrintStatus() #Good

        #Manual Print Needs Printer Working to Test
        if event == 'x_pos':
            try:
                move = int(values['-UNITVALUE-'])
                if move < 0:
                    sg.Popup("Please enter a valid, non-negative integer")
                else:
                    unit = (values['-UNITLIST-'])
                    manualPrint(move,'x_pos',unit)
            except:
                sg.popup("Please specify integer value")

        if event == 'x_neg':
            try:
                move = int(values['-UNITVALUE-'])
                if move < 0:
                    sg.Popup("Please enter a valid, non-negative integer")
                else:
                    unit = (values['-UNITLIST-'])
                    manualPrint(move,'x_neg',unit)
            except:
                sg.popup("Please specify integer value")
                
        if event == 'y_pos':
            try:
                move = int(values['-UNITVALUE-'])
                if move < 0:
                    sg.Popup("Please enter a valid, non-negative integer")
                else:
                    unit = (values['-UNITLIST-'])
                    manualPrint(move,'y_pos',unit)
            except:
                sg.popup("Please specify integer value")
                
        if event == 'y_neg':
            try:
                move = int(values['-UNITVALUE-'])
                if move < 0:
                    sg.Popup("Please enter a valid, non-negative integer")
                else:
                    unit = (values['-UNITLIST-'])
                    manualPrint(move,'y_neg',unit)
            except:
                sg.popup("Please specify integer value")
                
        if event == 'z_pos':
            try:
                move = int(values['-UNITVALUE-'])
                if move < 0:
                    sg.Popup("Please enter a valid, non-negative integer")
                else:
                    unit = (values['-UNITLIST-'])
                    manualPrint(move,'z_pos',unit)
            except:
                sg.popup("Please specify integer value")
                
        if event == 'z_neg':
            try:
                move = int(values['-UNITVALUE-'])
                if move < 0:
                    sg.Popup("Please enter a valid, non-negative integer")
                else:
                    unit = (values['-UNITLIST-'])
                    manualPrint(move,'z_neg',unit)
            except:
                sg.popup("Please specify integer value")
        
        else:
            continue

# Starts the program
printMenu()