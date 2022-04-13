# Define Specifications for coordinate template here:
# Measurements are all in mm.
length = 40                     # X Max
width = 40                      # Y Max
resolution = 10                  # Y Thickness
layer_thickness = 10             # Z Thickness

# Measurements have no units, must be at least 1
layers = 1

# How long each chunk is in mm.
chunk_length = 10        # X Thickness



##### FOLLOWING CODE GENERATES THE g_code #####


# Program Defines own fileName
fileName = str(length) + '_' + str(width) + '_' + str(layers) + '_gcode.txt'

# Calculates layers value for generating coords
layers -= 1

# Will generate a rectangular G code that can be used by printer interface
def cordGen():
    file = open(fileName,"w")
    x_path = 0
    y_path = 0
    z_path = 0
    current_layers = 0
    while current_layers <= layers:
        # Ascending Y_Path
        while y_path <= width:
            # Ascending X_Path
            while x_path <= length:
                file.write('G1 X' + str(x_path) + ' Y' + str(y_path) + ' Z' + str(z_path) + '\n')
                x_path += chunk_length
            
            if y_path == width:
                x_path -= chunk_length
                break
            
            x_path -= chunk_length
            y_path += resolution

            # Descending X_Path
            while x_path >= 0:
                file.write('G1 X' + str(x_path) + ' Y' + str(y_path) + ' Z' + str(z_path) + '\n')
                x_path -= chunk_length
            
            x_path += chunk_length
            y_path += resolution
        
        if current_layers == layers:
                break
        
        
        z_path += layer_thickness
        current_layers += 1
        
        # Descending Y_Path
        while y_path >= 0:
            # Ascending X_Path
            while x_path >= 0:
                file.write('G1 X' + str(x_path) + ' Y' + str(y_path) + ' Z' + str(z_path) + '\n')
                x_path -= chunk_length
            
            if y_path == 0:
                x_path += chunk_length
                break
            
            x_path += chunk_length
            y_path -= resolution

            # Descending X_Path
            while x_path <= length:
                file.write('G1 X' + str(x_path) + ' Y' + str(y_path) + ' Z' + str(z_path) + '\n')
                x_path += chunk_length
            
            x_path -= chunk_length
            y_path -= resolution


        z_path += layer_thickness
        current_layers += 1
        
    
    file.close()

### MUST BE DEFINED BEFORE PROGRAM IS RUN IN CURRENT ITERATION###
# Steps to MM ratio for specific printer software is being used on
x_conv = 0.0125
y_conv = 0.0125
z_conv = 0.0176

x_step = 1/x_conv
y_step = 1/y_conv
z_step = 1/z_conv

output = open("output.txt","w")

# Converts g_code file from MM to steps, rounds to the nearest step in
def conversion(contents):
    for item in contents:
        item[0] = round(item[0] * x_step)
        item[1] = round(item[1] * y_step)
        item[2] = round(item[2] * z_step)

# Loads file into array by line
def loadFile(file_path):
    try:    
        file = open(file_path)
        tempContents = file.readlines()
        return tempContents
    except:
        return -1

# Based on file calculates change rather than cords, outputs result to comma
def getChange(file):
    contents = loadFile(file)
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
    for item in newContents:
        output.write(str(item[0]) + "," + str(item[1]) + "," + str(item[2]) + "," + "\n")

cordGen()

getChange(fileName)