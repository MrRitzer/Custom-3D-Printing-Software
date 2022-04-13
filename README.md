# Custom-3D-Printing-Software
Repository for Dr. Ulvens Research Team at North Dakota State University. Contains custom made 3d printing frontend and backend.

## Arduino Printer Codes Files

__ArduinoPrinterCode__ - Simple printing based on manually controlling a driver using HIGH and LOW signals. _outdated_ 

__ArduinoPrinterCodeV2__ - Implemented AccelStepper for driver control. Operated by recieving every set of coordinates from host. _outdated_ 

__ArduinoPrinterCodeV3__ - Greatly improved upon V2, still relied on coordinates coming from host. _outdated_ 

__ArduinoPrinterCodeV4__ - Transitioned to using an sd card to read prints from, greatly improved on printing performance. However, was still bottlenecked by a timer from the host to keep the program on track. _outdated_ 

__ArduinoPrinterCodeV5__ - Transitioned to interrupt based serial communication rather than blocking. Ready to be implemented in any printer developed in a similar manner.

__ArduinoPrinterCodeV5.1_Lasers__ - Implemented using lasers on various axis in addition to x,y,z motion

__SD_Card_File_Copy__ - Program for testing with Sd cards.

__SD_Card_Read__ - Program for testing with Sd cards. _outdated_

__SD_Card_Read_2__ - Program for testing with Sd cards.

__staggered__ - Printing program. Not used with current system. File contains pinout information that was useful.

## Python Code Files

__arduinoV5__ - Helper class for interfaceV5 for use with ArduinoPrinterCodeV5. Similar to V4 but functionality was changed to reflect transition from blocking based communication to interrupt based communication.

__interfaceV5__ - GUI that was designed for use with ArdinoPrinterCodeV5. Visually similar to V4, backend functionality is slightly different being that the system transitioned to interrupt based commmunication

### Subfolder - Additional Components

__CoordinateGenUI__ - Provides an easy to use GUI for various functionality that can be implemented by printers when generating output files to put on their SD cards.

__PrinterCodeGenerator__ - Defines the methods used by CoordinateGenUI to take parameters provided by the user and convert that into output the printer can handle.

__GCodeConverter__ - Converts a Gcode (A simple Gcode albeit) into an output file for a printer. Could be tweaked to allow more complex prints to be created for the printer. _outdated_

__GCodeGenerator__ - Generates a rectangular Gcode (Once again, simple) file that can be given to GCodeConverter. _outdated_ 

### Subfolder - G_Code

Contains various G_code example files and a readme for tools required to run the Python interface that communicates with the arduino.

### Subfolder - Non-Sd

__arduino__ - Helper class used by interface for communication with the arduino controlling the printer.

__arduinoTesting__ - Dummy class that existed to help with testing GUI functionality without having to have physical access to a printer.

__arduinoV2__ - Helper class used by interfaceV2 for communication with the arduino controlling the printer.

__interface__ - First version of the GUI, designed for use with ArduinoPrinterCode to control printer movements.

__interfaceV2__ - Second version of GUI, designed for use with ArduinoPrinterVodeV2 to control printer movements.

### Subfolder - Old

__arduinoTestingV4__ - Dummy class for interfaceV4 that existed to help with testing GUI functionality without having to have physical access to a printer.

__arduinoV4__ - Helper class used by interfaceV4 for use with ArduinoPrinterCodeV4. Very different than previous versions due to transition to sd cards for prints rather than sending the print via serial.

__interfaceV4__ - GUI that was designed for use with ArduinoPrinterCodeV4. Functionally different than previous versions due to no longer ingesting a file to send over serial.
