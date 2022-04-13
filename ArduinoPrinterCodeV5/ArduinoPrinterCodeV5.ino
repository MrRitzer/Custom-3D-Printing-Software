/*
  This example shows how to read and write data to and from an SD card file
  The circuit:
   SD card attached to SPI bus as follows:
 ** MOSI - pin 11 or 51
 ** MISO - pin 12 or 50
 ** CLK - pin 13 or 52
 ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN) or 53
*/
#include <SPI.h>
#include <SD.h>
#include <AccelStepper.h>

//Defines three AccelStepper profiles for each motor
//Change to reflect printer setup
AccelStepper x_stepper(AccelStepper::DRIVER, 4, 5);
AccelStepper y_stepper(AccelStepper::DRIVER, 6, 38);
AccelStepper z_stepper(AccelStepper::DRIVER, 8, 9);

// Variables for within arduino code
int arr_pos = 0;
int rpm = 500;
int current_mode = 0;
int previous_mode = 0;
bool isDone = false;
int mnlMv[3] = {0,0,0};

//Variables used with the SD card
File myFile;
int RunCount = 0;
int xCords[500];
int yCords[500];
int zCords[500];

void setup() {
  x_stepper.setMaxSpeed(2000);
  x_stepper.setSpeed(rpm);
  x_stepper.setAcceleration(1000);
  y_stepper.setMaxSpeed(2000);
  y_stepper.setSpeed(rpm);
  y_stepper.setAcceleration(1000);
  z_stepper.setMaxSpeed(2000);
  z_stepper.setSpeed(rpm);
  z_stepper.setAcceleration(1000);
  SD.begin(53);
  Serial.begin(9600);
  GetSize();
  GetCords();
}

void loop() {
    recvData();
    prcsData();
    //Start Print
    if (current_mode == 1) {
      previous_mode = current_mode;
      if (!isDone) {
        autoPrint();
      }
      //Pause Print
      else {
        current_mode = 2;
      }
    }
    //Pause Print
    if (current_mode == 2) {
      previous_mode = current_mode;
    }
    //Stop Print
    if (current_mode == 3) {
      previous_mode = current_mode;
      arr_pos = 0;
      isDone = false;
      //Pause Print
      current_mode = 2;
    }
    //Go Home
    if (current_mode == 4) {
      x_stepper.runToNewPosition(0);
      y_stepper.runToNewPosition(0);
      z_stepper.runToNewPosition(0);
      //Pause Print
      current_mode = 2;
    }
    //Set Home
    if (current_mode == 5) {
      x_stepper.setCurrentPosition(0);
      y_stepper.setCurrentPosition(0);
      z_stepper.setCurrentPosition(0);
      //Pause Print
      current_mode = 2;
    }
    //Get Print Status
    if (current_mode == 6) {
      Serial.print(arr_pos + 1);
      Serial.print('/');
      Serial.print(RunCount); //Working
      if (previous_mode == 1) {
        //Start Print
        current_mode = 1;
      }
      else if (previous_mode == 3) {
        //Stop Print
        current_mode = 3;
      }
      else {
        //Pause Print
        current_mode = 2;
      }
    }
    //Manual Print
    if (current_mode == 7) {
      previous_mode = current_mode;
      recvData();
      prcsData();
      manualPrint();
      //Pause Print
      current_mode = 2;
    }
}

void manualPrint() {
  while (true) {
    if (mnlMv[0]+mnlMv[1]+mnlMv[2] == 0) {
      break;
    }
    if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0) {
      x_stepper.setCurrentPosition(0);
      x_stepper.moveTo(mnlMv[0]);
      x_stepper.setSpeed(rpm);
      y_stepper.setCurrentPosition(0);
      y_stepper.moveTo(mnlMv[1]);
      y_stepper.setSpeed(rpm);
      z_stepper.setCurrentPosition(0);
      z_stepper.moveTo((mnlMv[2] * -1));
      z_stepper.setSpeed(rpm);
    }
    else {
      x_stepper.runSpeedToPosition();
      y_stepper.runSpeedToPosition();
      z_stepper.runSpeedToPosition();
      if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0) {
        break;
      }
    }
  }
  mnlMv[0] = 0;
  mnlMv[1] = 0;
  mnlMv[2] = 0;
}

void autoPrint() {
  if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0 && arr_pos < RunCount) {
    x_stepper.setCurrentPosition(0);
    x_stepper.moveTo(xCords[arr_pos]);
    x_stepper.setSpeed(rpm);
    y_stepper.setCurrentPosition(0);
    y_stepper.moveTo(yCords[arr_pos]);
    y_stepper.setSpeed(rpm);
    z_stepper.setCurrentPosition(0);
    z_stepper.moveTo(zCords[arr_pos]);
    z_stepper.setSpeed(rpm);
    arr_pos++;
  }
  else if (arr_pos == RunCount) {
    isDone = true;
  }
  else {
    x_stepper.runSpeedToPosition();
    y_stepper.runSpeedToPosition();
    z_stepper.runSpeedToPosition();
  }
}

void GetSize() {
  myFile = SD.open("output.txt");
  char tempChar;
  while (myFile.available()) {
    tempChar = char(myFile.read());
    if (tempChar == '\n') {
      RunCount++;
    }
  }
  // close the file:
  myFile.close();
}

void GetCords() {
  myFile = SD.open("output.txt");
  char tempChar;
  int tempIntVal;
  String tempVal;
  String tempInt;
  for (int i = 0; i < RunCount; i++) {
    bool x = true;
    bool y = true;
    bool z = true;
    tempInt = "";
    tempVal = "";
    tempChar = 'a';
    while (true) {
      tempChar = char(myFile.read());
      if (tempChar == '\n') {
        break;
      }
      else {
        tempVal += tempChar;
      }
    }
    for (int j = 0; j < tempVal.length(); j++) {
      tempChar = tempVal[j];
      if (tempChar == ',' && x) {
        tempIntVal = tempInt.toInt();
        xCords[i] = tempIntVal;
        tempInt = "";
        x = false;
      }
      else if (tempChar == ',' && y) {
        tempIntVal = tempInt.toInt();
        yCords[i] = tempIntVal;
        tempInt = "";
        y = false;
      }
      else if (tempChar == ',' && z) {
        tempIntVal = tempInt.toInt();
        zCords[i] = tempIntVal;
        tempInt = "";
        z = false;
      }
      else {
        tempInt += tempChar;
      }
    }
  }
}

//Can recieve data up to 32 characters
const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false;

//Starts when called in Loop
//If no data is waiting at port proceeds without blocking
void recvData() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//If new data was flagged by the recvData reads
//in the new data. Otherwise exits without blocking
void prcsData() {
    if (newData == true) {
        char tempChar = 'a';
        int tempIntVal;
        String tempInt = "";
        bool x = true;
        bool y = true;
        bool z = true;
        if (strlen(receivedChars) > 1) {
          for (int j = 0; j < strlen(receivedChars); j++) {
            tempChar = receivedChars[j];
            if (tempChar == ',' && x) {
              tempIntVal = tempInt.toInt();
              mnlMv[0] = tempIntVal;
              tempInt = "";
              x = false;
            }
            else if (tempChar == ',' && y) {
              tempIntVal = tempInt.toInt();
              mnlMv[1] = tempIntVal;
              tempInt = "";
              y = false;
            }
            else if (tempChar == ',' && z) {
              tempIntVal = tempInt.toInt();
              mnlMv[2] = tempIntVal;
              tempInt = "";
              z = false;
            }
            else {
              tempInt += tempChar;
            }
          }
        }
        else {
          tempInt = receivedChars[0];
          tempIntVal = tempInt.toInt();
          current_mode = tempIntVal;
        }
        newData = false;
    }
}
