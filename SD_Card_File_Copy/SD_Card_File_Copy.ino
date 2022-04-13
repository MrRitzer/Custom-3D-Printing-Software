#include <SPI.h>
#include <SD.h>

char* file_name1 = "output.txt";
char* file_name2 = "temp.txt";
byte ibuffer[3000];
int ibufferspace = sizeof(ibuffer);
File File1;
File File2;

void setup() {
 Serial.begin(9600);
 Serial.print("Initializing SD card...");
 pinMode(4, OUTPUT);
 
 if (!SD.begin(4)) {
   Serial.println("Initialization failed!");
   return;
 }else {
   Serial.println("Initialization done.");
 }

 File1 = SD.open(file_name1);
 if (File1) {
   Serial.println("Opening the file: " + String(file_name1) + " done.");
 }else {
   Serial.println("Error opening " + String(file_name1));
 }

 if(SD.exists(file_name2)) {
   SD.remove(file_name2);
   Serial.println("File :" + String(file_name2) + " deleted...");
 }

 unsigned int previoustime = millis();
 if (File1) {
    File2 = SD.open(file_name2, FILE_WRITE);
    if (File2) {
      while (File1.available() > 0)
      {
        int i = File1.readBytes(ibuffer, 64);
        File2.write(ibuffer, i);
      }
      // done, close the destination file
      File2.close();
    }
    Serial.println("Done copying...");
    // done, close the source file
    File1.close();
  }
 Serial.println("Time: " + String((millis()-previoustime)/1000) + " seg");
}

void loop()
{
 // nothing happens after setup
}
