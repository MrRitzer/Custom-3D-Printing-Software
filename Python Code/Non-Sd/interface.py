import PySimpleGUI as sg
import arduino as ar
from threading import Thread

image_zup = 'button_icons\\white_double_arrow_up.png'
image_zdn = 'button_icons\\white_double_arrow_down.png'
image_yup = 'button_icons\\white_arrow_up.png'
image_ydn = 'button_icons\\white_arrow_down.png'
image_xlf = 'button_icons\\white_arrow_left.png'
image_xrt = 'button_icons\\white_arrow_right.png'
image_tsp = 'button_icons\\transparent.png'

units = {'μm.','mm.'}

### MUST BE DEFINED BEFORE PROGRAM IS RUN IN CURRENT ITERATION###
# Steps to MM ratio for specific printer software is being used on
x_conv = 0.0125
y_conv = 0.0125
z_conv = 0.0176

x_step = 1/x_conv
y_step = 1/y_conv
z_step = 1/z_conv

# Converts g_code from MM to steps, rounds to the nearest step
def conversion(contents):
    for item in contents:
        item[0] = round(item[0] * x_step)
        item[1] = round(item[1] * y_step)
        item[2] = round(item[2] * z_step)

# Converts MM to steps, rounds to nearest step
def manualConversion(move, dir):
    if dir == 'x':
        return round(move * x_step)
    if dir == 'y':
        return round(move * y_step)
    if dir == 'z':
        return round(move * z_step)

# Loads file into array by line
def loadFile(file_path):
    try:    
        file = open(file_path)
        tempContents = file.readlines()
        return tempContents
    except:
        sg.popup("File not loaded")
        return -1

# Helper method for getting change from cords
def parseCord(item):
    cord_split = item.split()

# Based on file calculates change rather than cords
def getChange():
    newContents = []
    temp_x1 = 0
    temp_y1 = 0
    temp_z1 = 0
    runs = 0
    for item in contents:
        item_split = item.split(' ')
        if runs == 0:
            temp_x1 = int(item_split[1][1:])
            temp_y1 = int(item_split[2][1:])
            temp_z1 = int(item_split[3][1:])
        else: 
            temp_x2 = int(item_split[1][1:])
            temp_y2 = int(item_split[2][1:])
            temp_z2 = int(item_split[3][1:])
            change_x = temp_x2 - temp_x1
            change_y = temp_y2 - temp_y1
            change_z = temp_z2 - temp_z1
            newContents.append([change_x,change_y,change_z])
            temp_x1 = temp_x2
            temp_y1 = temp_y2
            temp_z1 = temp_z2
        runs += 1
    conversion(newContents)
    return newContents

# Sets icon image size for gui
def getImg(x,y):
    return sg.Image(source=image_tsp,size=(x,y))

# Pausable Print method for controlling stepper motors
def printCords(stop):
    # Gives access to used global variables
    global contents
    global print_index
    global print_status
    global is_paused
    global contLen

    working_status = True

    while contents:  
        if exit_flag:
            is_paused = True
            return
        if working_status == False:
            break
        else:
            item = contents.pop(0)
            print("Pass",print_index + 1, "of",contLen)
            x_cord = item[0]
            y_cord = item[1]
            z_cord = item[2]
            if x_cord < 0:
                x_dir = 0
                x_cord = abs(x_cord)
            else:
                x_dir = 1

            if y_cord < 0:
                y_dir = 0
                y_cord = abs(x_cord)
            else:
                y_dir = 1

            if z_cord < 0:
                z_dir = 0
                z_cord = abs(x_cord)
            else:
                z_dir = 1

            # Initial waiting for response
            waiting_status = True
            while waiting_status:
                ar.set_num(int(x_cord),int(y_cord),int(z_cord),int(x_dir),int(y_dir),int(z_dir))
                status = int(z_cord) + 1
                # Verifies connection with Arduino
                response = ar.write_read()
                if (response == status):
                    waiting_status = False
                elif (response == -15.5):
                    waiting_status = False
                    working_status = False   
                    sg.popup('Arduino timed out')
            # Verifies arduino recieved
            if working_status == False:
                break
            # Waiting for confirmation that print completed
            waiting_status = True

            while waiting_status:
                response = ar.read()
                status = (int(z_cord) + 3)
                if (response == status):
                    waiting_status = False
                elif (response == -15.5):
                    waiting_status = False
                    working_status = False   
                    sg.popup('Arduino failed on print')
            
            # Verifies arduino recieved
            if working_status == False:
                break

            print_index += 1
            if x_dir == 0:
                currentPosition[0] += (x_cord * -1)
            else: 
                currentPosition[0] += (x_cord * 1)
            if y_dir == 0:
                currentPosition[1] += (y_cord * -1)
            else:
                currentPosition[1] += (y_cord * 1)
            if z_dir == 0:
                currentPosition[2] += (z_cord * -1)
            else:
                currentPosition[2] += (z_cord * 1)
    print("Print complete!")
    print_index = 0
    contents = 'Empty'
    is_paused = False
    print_status = False
    waiting_status = False
    working_status = False   
    contLen = 0

# Manual print method for manually controlling stepper motors
def manualPrint(move, dir, unit):
    if unit == 'μm.':
        move = move / 1000
    if dir == "x_pos":
        move = manualConversion(move,'x')
        currentPosition[0] += (move * 1)
        ar.set_num(move,0,0,1,1,1)
        ar.manual_write()
    if dir == "x_neg":
        move = manualConversion(move,'x')
        currentPosition[0] += (move * -1)
        ar.set_num(move,0,0,0,1,1)
        ar.manual_write()
    if dir == "y_pos":
        move = manualConversion(move,'y')
        currentPosition[1] += (move * 1)
        ar.set_num(0,move,0,1,1,1)
        ar.manual_write()
    if dir == "y_neg":
        move = manualConversion(move,'y')
        currentPosition[1] += (move * -1)
        ar.set_num(0,move,0,1,0,1)
        ar.manual_write()
    if dir == "z_pos":
        move = manualConversion(move,'z')
        currentPosition[2] += (move * 1)
        ar.set_num(0,0,move,1,1,1)
        ar.manual_write()
    if dir == "z_neg":
        move = manualConversion(move,'z')
        currentPosition[2] += (move * -1)
        ar.set_num(0,0,move,1,1,0)
        ar.manual_write()

# Moves back to starting position
def moveHome():
    unit = "mm"
    move = 0 - currentPosition[0]
    if move < 0:
        dir = "x_neg"
        move = abs(move)
        move = move / x_step
    else:
        dir = "x_pos"
        move = move / x_step
    manualPrint(move,dir,unit)
    currentPosition[0] = 0
    move = 0 - currentPosition[1]
    if move < 0:
        dir = "y_neg"
        move = abs(move)
        move = move / y_step
    else:
        dir = "y_pos"
        move = move / y_step
    manualPrint(move,dir,unit)
    currentPosition[1] = 0
    move = 0 - currentPosition[2]
    if move < 0:
        dir = "z_neg"
        move = abs(move)
        move = move / z_step
    else:
        dir = "z_pos"
        move = move / z_step
    manualPrint(move,dir,unit)
    currentPosition[2] = 0

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

                [sg.B('Load File'),sg.B('Set Home'),sg.B('To Home')],

                [sg.B('Start Print'), sg.B('Pause Print'), sg.B('Resume Print'), sg.B('Stop Print'), sg.B('Quit')]
                
                 ]

    # Create the window 
    window = sg.Window('3d Printer Interface', menu)

    # Initializes status'
    global print_status 
    print_status = False

    # Initialize Index in case of pause
    global print_index
    print_index = 0

    # Initialize contents as empty
    global contents
    contents = 'Empty'

    # Initialize exit_flag
    global exit_flag
    exit_flag = False

    # Initialize is paused
    global is_paused
    is_paused = False

    # Initialize length of contents
    global contLen
    contLen = 0

    # Global for home and current position so manual print
    # Can calculate distance to move to get to home, home will always
    # Be 0,0,0 but current position will get set to home if set home
    # is called
    global currentPosition
    currentPosition = [0,0,0]
    

    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            if print_status == True and sg.popup_ok_cancel("Do you really want to exit?", title="Confirm exit") == "OK":
                ar.close()
                break
            if print_status == False:
                ar.close()
                break
            else:
                printMenu()
                break
        
        if event == 'Start Print':
            if contents == 'Empty':
                sg.popup('File not loaded')
            else:
                # Starts print in a thread so user can interrupt if necessary
                print_status = True
                printThread = Thread(target=printCords, args=(lambda: exit_flag,))
                printThread.start()
        
        if event == 'Load File':
            file_name = sg.popup_get_file('Select G-Code file to load')
            contents = loadFile(file_name)
            if contents == -1:
                contents = 'Empty'
            else:
                contents = getChange()
                for item in contents:
                    contLen += 1
        
        if event == 'Resume Print':
            if is_paused:
                exit_flag = False
                printThread = Thread(target=printCords, args=(lambda: exit_flag,))
                printThread.start()
                is_paused = False
            else:
                sg.popup("No current print paused")
        
        if event == 'Pause Print':
            if print_status:
                exit_flag = True
                printThread.join()
                sg.popup("Print paused")
            else:
                sg.popup("No current print in progress")
        
        if event == 'Stop Print':
            if print_status:
                exit_flag = True
                printThread.join()
                contents = 'Empty'
                exit_flag = False
                print_status = False
                is_paused = False
                print_index = 0
                contLen = 0
                sg.popup("Print stopped")
            else:
                sg.popup("No current print in progress")
        
        if event == 'Set Home':
            currentPosition = [0,0,0]
            sg.popup("Home is set to current position!")

        if event == 'To Home':
            if currentPosition == [0,0,0]:
                sg.popup('Already at home!')
            else:
                moveHome()
            
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