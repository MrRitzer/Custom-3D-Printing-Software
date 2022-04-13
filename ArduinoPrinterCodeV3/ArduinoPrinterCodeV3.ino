#include <AccelStepper.h>

//Defines three AccelStepper profiles for each motor
AccelStepper x_stepper(AccelStepper::DRIVER,6,7);
AccelStepper y_stepper(AccelStepper::DRIVER,4,5);
AccelStepper z_stepper(AccelStepper::DRIVER,8,9);

// Variables for back and forth between program
int x_steps = 0;
int y_steps = 0;
int z_steps = 0;

// Variables only for within arduino code
int rpm = 100;
int x_current_pos = 0;
int y_current_pos = 0;
int z_current_pos = 0;
bool mode = false;
bool printing = false;
bool last = false;
bool timeout = false;

void setup() {  
  x_stepper.setMaxSpeed(rpm*10);
  x_stepper.setSpeed(rpm);
  y_stepper.setMaxSpeed(rpm*10);
  y_stepper.setSpeed(rpm);
  z_stepper.setMaxSpeed(rpm*10);
  z_stepper.setSpeed(rpm);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()>0) {
    if (x_steps == 0 && y_steps == 0 && z_steps == 0) {
      getMode();
      getCords();
    }
    x_stepper.runSpeedToPosition();
    y_stepper.runSpeedToPosition();
    z_stepper.runSpeedToPosition();
  }
}

void manualPrint() {
  if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0) {
    x_stepper.setCurrentPosition(0);
    x_stepper.moveTo(x_steps);
    x_stepper.setSpeed(rpm);
    y_stepper.setCurrentPosition(0);
    y_stepper.moveTo(y_steps);
    y_stepper.setSpeed(rpm);
    z_stepper.setCurrentPosition(0);
    z_stepper.moveTo((z_steps * -1));
    z_stepper.setSpeed(rpm);
  }
  else {
    x_stepper.runSpeedToPosition();
    y_stepper.runSpeedToPosition();
    z_stepper.runSpeedToPosition();
    if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0) {
      printing = false;
    }
  }
}

void autoPrint() {
  if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0) {
    x_stepper.setCurrentPosition(0);
    x_stepper.moveTo(x_steps);
    x_stepper.setSpeed(rpm);
    x_current_pos = x_steps;
    y_stepper.setCurrentPosition(0);
    y_stepper.moveTo(y_steps);
    y_stepper.setSpeed(rpm);
    y_current_pos = y_steps;
    z_stepper.setCurrentPosition(0);
    z_stepper.moveTo((z_steps * -1));
    z_stepper.setSpeed(rpm);
    z_current_pos = z_steps;
  }
  if (x_current_pos == x_steps && y_current_pos == y_steps && z_current_pos == z_steps && !last) {
    getMode();
    getCords();
    if (timeout == true) {
      reset();
    }
    else {
      Serial.print(z_steps + 3);
    }
  }
  else {
    x_stepper.runSpeedToPosition();
    y_stepper.runSpeedToPosition();
    z_stepper.runSpeedToPosition();
    if (x_stepper.distanceToGo() == 0 && y_stepper.distanceToGo() == 0 && z_stepper.distanceToGo() == 0 && last) {
      printing = false;
    }
  }
}

void reset() {
  x_steps = 0;
  y_steps = 0;
  z_steps = 0;
  x_current_pos = 0;
  y_current_pos = 0;
  z_current_pos = 0;
  last = false;
  mode = false;
  timeout == false;
}

// Get cords from program
void getCords() { 
  x_steps = read_int();
  y_steps = read_int();
  z_steps = read_int();
}
void getMode() {
  int temp = read_int();
  if (temp == 2) {
    mode = true;
    last = true;
  }
  if (temp == 1) {
    mode = true;
    last = false;
  }
  if (temp == 0 ) {
    mode = false;
    last = false;
  }
}

// Used to convert numbers sent from program to Arduino
#define TO_INT32(a,b,c,d) (((d)<<24)|((c)<<16)|((b)<<8)|(a))
int32_t read_int()
{
  uint32_t result[4];
  for (int i = 0; i < 4; i++) {
    unsigned long st = millis();
    // Wait for data at the port
    while (!Serial.available()) {
      unsigned long t = millis();
      if ( ( ( t - st ) / 1000 ) >= 5 ) {
        timeout = true;
        break;
      }
      else {
        continue;
      }
    }
    if (timeout == true) {
      reset();
      return TO_INT32(0,0,0,0);
    }
    result[i] = Serial.read();
  }
  reset();
  return TO_INT32(result[0], result[1], result[2], result[3]);
}
