/*
This example shows how to read and write data to and from an SD card file
  The circuit:
   SD card attached to SPI bus as follows:
 ** MOSI - pin 11 or 51
 ** MISO - pin 12 or 50
 ** CLK - pin 13 or 52
 ** CS - pin 4 (for MKRZero SD: SDCARD_SS_PIN)
*/
#include <SPI.h>
#include <SD.h>

File myFile;
int RunCount = 0;
int xCords[100];
int yCords[100];
int zCords[100];

void setup() {
  // Open serial communications and wait for port to open:
  SD.begin(53);
  Serial.begin(9600);
  GetSize();
}
   
void loop() {
  GetCords();
  for (int i=0; i<RunCount; i++) {
    Serial.print("Num: ");
    Serial.print(i+1);
    Serial.print(" ");
    Serial.print(xCords[i]);
    Serial.print(",");
    Serial.print(yCords[i]);
    Serial.print(",");
    Serial.print(zCords[i]);
    Serial.print(",");
    Serial.println();
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
