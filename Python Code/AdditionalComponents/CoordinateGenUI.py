import PySimpleGUI as sg
import PrinterCodeGenerator as pg
from os.path import exists
# Starts the menu with an initial print status
def coordMenu(): 
    menu = [[sg.Checkbox('Length:',key='-LENGTHCB-',default=True,enable_events=True),sg.Input(key='-LENGTH-',size=(5,5),disabled_readonly_background_color='#979392'),sg.Text('   Chunk Length:'),sg.Input(key='-CHUNKLENGTH-',size=(5,5),disabled_readonly_background_color='#979392'),sg.Text('X Step to MM:'),sg.Input(key='-XCONV-',size=(10,5),disabled_readonly_background_color='#979392')],
    
            [sg.Checkbox('Width: ',key='-WIDTHCB-',default=True,enable_events=True),sg.Input(key='-WIDTH-',size=(5,5),disabled_readonly_background_color='#979392'),sg.Text('        Resolution:'),sg.Input(key='-RESOLUTION-',size=(5,5),disabled_readonly_background_color='#979392'),sg.Text('Y Step to MM:'),sg.Input(key='-YCONV-',size=(10,5),disabled_readonly_background_color='#979392')],

            [sg.Checkbox('Layers:',key='-LAYERCB-',default=True,enable_events=True),sg.Input(key='-LAYERS-',size=(5,5),disabled_readonly_background_color='#979392'),sg.Text('Layer Thickness:'),sg.Input(key='-LAYERTHICKNESS-',size=(5,5),disabled_readonly_background_color='#979392'),sg.Text('Z Step to MM:'),sg.Input(key='-ZCONV-',size=(10,5),disabled_readonly_background_color='#979392')],

            [sg.Checkbox('Lasers?', key='-LASERS-')],

            [sg.Text('Filename:'),sg.Input("output.txt",key='-FILENAME-',size=(8,5),disabled=True,disabled_readonly_background_color='#979392')],

            [sg.B('Generate'), sg.B('Load Last Output'), sg.B('Quit')]]

    # Create the window 
    window = sg.Window('Coordinate Generator', menu)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == '-LENGTHCB-':
            if values['-LENGTHCB-'] == True:
                window.find_element('-LENGTH-').Update(disabled = False,value='')
                window.find_element('-CHUNKLENGTH-').Update(disabled = False,value='')
                window.find_element('-XCONV-').Update(disabled = False,value='')
            if values['-LENGTHCB-'] == False:
                window.find_element('-LENGTH-').Update(disabled = True,value='')
                window.find_element('-CHUNKLENGTH-').Update(disabled = True,value='')
                window.find_element('-XCONV-').Update(disabled = True,value='')

        if event == '-WIDTHCB-':
            if values['-WIDTHCB-'] == True:
                window.find_element('-WIDTH-').Update(disabled = False,value='')
                window.find_element('-RESOLUTION-').Update(disabled = False,value='')
                window.find_element('-YCONV-').Update(disabled = False,value='')
            if values['-WIDTHCB-'] == False:
                window.find_element('-WIDTH-').Update(disabled = True,value='')
                window.find_element('-RESOLUTION-').Update(disabled = True,value='')
                window.find_element('-YCONV-').Update(disabled = True,value='')

        if event == '-LAYERCB-':
            if values['-LAYERCB-'] == True:
                window.find_element('-LAYERS-').Update(disabled = False,value='')
                window.find_element('-LAYERTHICKNESS-').Update(disabled = False,value='')
                window.find_element('-ZCONV-').Update(disabled = False,value='')
            if values['-LAYERCB-'] == False:
                window.find_element('-LAYERS-').Update(disabled = True,value='')
                window.find_element('-LAYERTHICKNESS-').Update(disabled = True,value='')
                window.find_element('-ZCONV-').Update(disabled = True,value='')
        
        if event == 'Generate':
            if values['-LASERS-'] == True:
                try:
                    pg.LaserCoordGen(float(values['-LENGTH-']),float(values['-CHUNKLENGTH-']),float(values['-XCONV-']),float(values['-WIDTH-']),float(values['-RESOLUTION-']),float(values['-YCONV-']),float(values['-LAYERS-']),float(values['-LAYERTHICKNESS-']),float(values['-ZCONV-']),values['-FILENAME-'])
                    file = open('.temp_log','w')
                    file.write(str(values['-LENGTH-'])+"\n")
                    file.write(str(values['-CHUNKLENGTH-'])+"\n")
                    file.write(str(values['-XCONV-'])+"\n")
                    file.write(str(values['-WIDTH-'])+"\n")
                    file.write(str(values['-RESOLUTION-'])+"\n")
                    file.write(str(values['-YCONV-'])+"\n")
                    file.write(str(values['-LAYERS-'])+"\n")
                    file.write(str(values['-LAYERTHICKNESS-'])+"\n")
                    file.write(str(values['-ZCONV-'])+"\n")
                    file.close()
                except:
                    sg.popup_error("Verify all values are correct and try again",title="Error")
            else:
                try:
                    pg.DefaultCoordGen(float(values['-LENGTH-']),float(values['-CHUNKLENGTH-']),float(values['-XCONV-']),float(values['-WIDTH-']),float(values['-RESOLUTION-']),float(values['-YCONV-']),float(values['-LAYERS-']),float(values['-LAYERTHICKNESS-']),float(values['-ZCONV-']),values['-FILENAME-'])
                    file = open('.temp_log','w')
                    file.write(str(values['-LENGTH-'])+"\n")
                    file.write(str(values['-CHUNKLENGTH-'])+"\n")
                    file.write(str(values['-XCONV-'])+"\n")
                    file.write(str(values['-WIDTH-'])+"\n")
                    file.write(str(values['-RESOLUTION-'])+"\n")
                    file.write(str(values['-YCONV-'])+"\n")
                    file.write(str(values['-LAYERS-'])+"\n")
                    file.write(str(values['-LAYERTHICKNESS-'])+"\n")
                    file.write(str(values['-ZCONV-'])+"\n")
                    file.close()
                except:
                    sg.popup_error("Verify all values are correct and try again",title="Error")

        if event == 'Load Last Output':
            if exists(".temp_log"):
                file = open('.temp_log','r')
                window.find_element('-LENGTH-').Update(value=float(file.readline()))
                window.find_element('-CHUNKLENGTH-').Update(value=float(file.readline()))
                window.find_element('-XCONV-').Update(value=float(file.readline()))
                window.find_element('-WIDTH-').Update(value=float(file.readline()))
                window.find_element('-RESOLUTION-').Update(value=float(file.readline()))
                window.find_element('-YCONV-').Update(value=float(file.readline()))
                window.find_element('-LAYERS-').Update(value=float(file.readline()))
                window.find_element('-LAYERTHICKNESS-').Update(value=float(file.readline()))
                window.find_element('-ZCONV-').Update(value=float(file.readline()))
                file.close()
            else:
                sg.popup_error("No Prior Output Exists",title="Error")

        else:
            continue

# Starts the program
coordMenu()