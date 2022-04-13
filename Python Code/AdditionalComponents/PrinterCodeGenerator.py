# Will generate a rectangular G code that can be used by printer interface
# Contains an X,Y,Z and nothing else
# Example run
# DefaultCoordGen(40,10,0.0125,40,10,0.0125,1,10,0.0176,'output.txt')
def DefaultCoordGen(length,chunkLength,xConv,width,resolution,yConv,layers,layerThickness,zConv,filename):
    xPos = 0
    yPos = 0
    zPos = 0
    xCoords = []
    yCoords = []
    zCoords = []
    currentLayer = 1
    while currentLayer <= layers:
        # Ascending yPos
        while yPos <= width:
            # Ascending xPos
            while xPos <= length:
                xCoords.append(xPos)
                yCoords.append(yPos)
                zCoords.append(zPos)
                xPos += chunkLength
            
            if yPos == width:
                xPos -= chunkLength
                break
            
            xPos -= chunkLength
            yPos += resolution

            # Descending xPos
            while xPos >= 0:
                xCoords.append(xPos)
                yCoords.append(yPos)
                zCoords.append(zPos)
                xPos -= chunkLength
            
            xPos += chunkLength
            yPos += resolution
        
        if currentLayer == layers:
            break
        
        zPos += layerThickness
        currentLayer += 1
        
        # Descending yPos
        while yPos >= 0:
            # Ascending xPos
            while xPos >= 0:
                xCoords.append(xPos)
                yCoords.append(yPos)
                zCoords.append(zPos)
                xPos -= chunkLength
            
            if yPos == 0:
                xPos += chunkLength
                break
            
            xPos += chunkLength
            yPos -= resolution

            # Descending xPos
            while xPos <= length:
                xCoords.append(xPos)
                yCoords.append(yPos)
                zCoords.append(zPos)
                xPos += chunkLength
            
            xPos -= chunkLength
            yPos -= resolution


        zPos += layerThickness
        currentLayer += 1
    
    # Convert x coordinate points into steps
    for x in range(len(xCoords)):
        xCoords[x] = round(xCoords[x] / xConv)

    # Convert y coordinate points into steps
    for y in range(len(yCoords)):
        yCoords[y] = round(yCoords[y] / yConv)

    # Convert z coordinate points into steps
    for z in range(len(zCoords)):
        zCoords[z] = round(zCoords[z] / zConv)

    temp = 0
    tempXCoords = []
    # Convert x steps array into change array
    for x in range(len(xCoords)):
        if x == 0:
            temp = xCoords[x]
        else:
            tempXCoords.append(xCoords[x]-temp)
            temp = xCoords[x]

    tempYCoords = []
    # Convert y steps array into change array
    for y in range(len(yCoords)):
        if y == 0:
            temp = yCoords[y]
        else:
            tempYCoords.append(yCoords[y]-temp)
            temp = yCoords[y]

    # Convert z steps array into change array
    tempZCoords = []
    for z in range(len(zCoords)):
        if z == 0:
            temp = zCoords[z]
        else:
            tempZCoords.append(zCoords[z]-temp)
            temp = zCoords[z]
    
    # Writes change to file
    file = open(filename,"w")
    for i in range(len(tempXCoords)):
        file.write(str(tempXCoords[i]) + "," + str(tempYCoords[i]) + "," + str(tempZCoords[i]) + "," + "\n")
    file.close()

# Will generate a rectangular G code that can be used by printer interface
# Contains an X,Y,Z with a corresponding laser for each axis and nothing else
# Example run
# LaserCoordGen(40,10,0.0125,40,10,0.0125,1,10,0.0176,'output.txt')
def LaserCoordGen(length,chunkLength,xConv,width,resolution,yConv,layers,layerThickness,zConv,filename):
    xPos = 0
    yPos = 0
    zPos = 0
    xCoords = []
    yCoords = []
    zCoords = []
    currentLayer = 1
    while currentLayer <= layers:
        # Ascending yPos
        while yPos <= width:
            # Ascending xPos
            while xPos <= length:
                xCoords.append(xPos)
                yCoords.append(yPos)
                zCoords.append(zPos)
                xPos += chunkLength
            
            if yPos == width:
                xPos -= chunkLength
                break
            
            xPos -= chunkLength
            yPos += resolution

            # Descending xPos
            while xPos >= 0:
                xCoords.append(xPos)
                yCoords.append(yPos)
                zCoords.append(zPos)
                xPos -= chunkLength
            
            xPos += chunkLength
            yPos += resolution
        
        if currentLayer == layers:
            break
        
        zPos += layerThickness
        currentLayer += 1
        
        # Descending yPos
        while yPos >= 0:
            # Ascending xPos
            while xPos >= 0:
                xCoords.append(xPos)
                yCoords.append(yPos)
                zCoords.append(zPos)
                xPos -= chunkLength
            
            if yPos == 0:
                xPos += chunkLength
                break
            
            xPos += chunkLength
            yPos -= resolution

            # Descending xPos
            while xPos <= length:
                xCoords.append(xPos)
                yCoords.append(yPos)
                zCoords.append(zPos)
                xPos += chunkLength
            
            xPos -= chunkLength
            yPos -= resolution


        zPos += layerThickness
        currentLayer += 1
    
    # Convert x coordinate points into steps
    for x in range(len(xCoords)):
        xCoords[x] = round(xCoords[x] / xConv)

    # Convert y coordinate points into steps
    for y in range(len(yCoords)):
        yCoords[y] = round(yCoords[y] / yConv)

    # Convert z coordinate points into steps
    for z in range(len(zCoords)):
        zCoords[z] = round(zCoords[z] / zConv)

    xLaser = []
    yLaser = []
    zLaser = []
    
    temp = 0
    tempXCoords = []
    # Convert x steps array into change array
    for x in range(len(xCoords)):
        if x == 0:
            temp = xCoords[x]
        else:
            if (xCoords[x]-temp) != 0 and x:
                xLaser.append(1)
            else:
                xLaser.append(0)
            tempXCoords.append(xCoords[x]-temp)
            temp = xCoords[x]

    tempYCoords = []
    # Convert y steps array into change array
    for y in range(len(yCoords)):
        if y == 0:
            temp = yCoords[y]
        else:
            if (yCoords[y]-temp) != 0:
                yLaser.append(1)
            else:
                yLaser.append(0)
            tempYCoords.append(yCoords[y]-temp)
            temp = yCoords[y]

    # Convert z steps array into change array
    tempZCoords = []
    for z in range(len(zCoords)):
        if z == 0:
            temp = zCoords[z]
        else:
            if (zCoords[z]-temp) != 0:
                zLaser.append(1)
            else:
                zLaser.append(0)
            tempZCoords.append(zCoords[z]-temp)
            temp = zCoords[z]
    
    # Writes change to file
    file = open(filename,"w")
    for i in range(len(tempXCoords)):
        file.write(str(tempXCoords[i]) + "," + str(tempYCoords[i]) + "," + str(tempZCoords[i]) + "," + str(xLaser[i]) + "," + str(yLaser[i]) + "," + str(zLaser[i]) + "," + "\n")
    file.close()