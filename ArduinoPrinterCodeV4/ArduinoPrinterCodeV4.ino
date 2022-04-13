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
AccelStepper x_stepper(AccelStepper::DRIVER, 4, 5);
AccelStepper y_stepper(AccelStepper::DRIVER, 6, 7);
AccelStepper z_stepper(AccelStepper::DRIVER, 8, 9);

// Variables for within arduino code
int arr_pos = 0;
int rpm = 500;
int x_step;
int y_step;
int z_step;
int current_mode = 0;
int previous_mode = 0;
bool isDone = false;
unsigned long st;
unsigned long ct;

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
  st = millis();
}

void loop() {
  if (Serial.available() > 0) {
    int temp = 7;
//    ct = millis();
//    if (( ( ct - st ) / 1000 ) >= 0.75) {
//      st = millis();
//      temp = read_int();
//    }
    if (temp > 0) {
      current_mode = temp;
    }

    if (current_mode == 13) {
      previous_mode = current_mode;
      temp = 0;
    }

    if (current_mode == 1) {
      previous_mode = current_mode;
      x_step = read_int();
      y_step = read_int();
      z_step = read_int();
      if ( read_int() == 1) {
        Serial.println("Its 1!");
        x_step = x_step * 1;
      }
      else {
        Serial.println("Its 0!");
        x_step = x_step * -1;
      }
      
      if ( read_int() == 1) {
        y_step = y_step * 1;
      }
      else {
        y_step = y_step * -1;
      }
      
      if ( read_int() == 1) {
        z_step = z_step * 1;
      }
      else {
        z_step = z_step * -1;
      }
      manualPrint();
      current_mode = 13;
      Serial.print(x_step);
      Serial.print('-');
      Serial.print(y_step);
      Serial.print('-');
      Serial.print(z_step);
    }

    if (current_mode == 2) {
      Serial.print(arr_pos + 1);
      Serial.print('/');
      Serial.print(RunCount); //Working
      if (previous_mode == 4) {
        current_mode = 4;
      }
      else if (previous_mode == 6) {
        current_mode = 6;
      }
      else {
        current_mode = 13;
      }
    }

    if (current_mode == 3) {
      //Serial.print(3); Working
      x_stepper.runToNewPosition(0);
      y_stepper.runToNewPosition(0);
      z_stepper.runToNewPosition(0);
      current_mode = 13;
    }

    if (current_mode == 4) {
      previous_mode = current_mode;
      if (!isDone) {
        autoPrint();
      }
      else {
        current_mode = 13;
      }
    }

    if (current_mode == 5) {
      x_stepper.setCurrentPosition(0);
      y_stepper.setCurrentPosition(0);
      z_stepper.setCurrentPosition(0);
      current_mode = 13;
      //Serial.print(5); Working
    }

    if (current_mode == 6) {
      previous_mode = current_mode;
      arr_pos = 0;
      isDone = false;
      current_mode = 13;
      //Serial.print(6); Working
    }

    if (current_mode == 7) {
        autoPrint();
    }
  }
}

void manualPrint() {
  bool moving = true;
  while (moving) {
    if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0) {
      x_stepper.setCurrentPosition(0);
      x_stepper.moveTo(x_step);
      x_stepper.setSpeed(rpm);
      y_stepper.setCurrentPosition(0);
      y_stepper.moveTo(y_step);
      y_stepper.setSpeed(rpm);
      z_stepper.setCurrentPosition(0);
      z_stepper.moveTo((z_step * -1));
      z_stepper.setSpeed(rpm);
    }
    else {
      x_stepper.runSpeedToPosition();
      y_stepper.runSpeedToPosition();
      z_stepper.runSpeedToPosition();
    if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0) {
      moving = false;
    }
  }
  }
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

// Used to convert numbers sent from program to Arduino
#define TO_INT32(a,b,c,d) (((d)<<24)|((c)<<16)|((b)<<8)|(a))
int32_t read_int()
{
  uint32_t result[4];
  for (int i = 0; i < 4; i++) {
    // Wait for data at the port
    while (!Serial.available());
    result[i] = Serial.read();
  }
  return TO_INT32(result[0], result[1], result[2], result[3]);
}
