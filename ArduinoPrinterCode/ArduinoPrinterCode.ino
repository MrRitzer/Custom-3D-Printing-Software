int x_motor_direction = 7; //Direction Pin
int x_motor_step = 6;  //Stepper Pin
int y_motor_direction = 5; //Direction Pin
int y_motor_step = 4;  //Stepper Pin
int z_motor_direction = 9; //Direction Pin
int z_motor_step = 8;  //Stepper Pin
int x_steps = 0;
int y_steps = 0;
int z_steps = 0;
int x_dir = 0;
int y_dir = 0;
int z_dir = 0;
int results = 0;
int dl = 1;

void setup() {
  // put your setup code here, to run once:
  pinMode(x_motor_direction, OUTPUT);
  pinMode(x_motor_step, OUTPUT);
  pinMode(y_motor_direction, OUTPUT);
  pinMode(y_motor_step, OUTPUT);
  pinMode(z_motor_direction, OUTPUT);
  pinMode(z_motor_step, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available()>0) {
      // First three sent numbers are x, y and z movements respectively
      x_steps = read_int();
      y_steps = read_int();
      z_steps = read_int();

      // Second three numbers are x, y and z motor directions respictively
      x_dir = read_int();
      y_dir = read_int();
      z_dir = read_int();
      
      results = z_steps + 1;
      Serial.print(results);

      // Moves x motor
      for (int i = 0; i < x_steps; i++){
        //Sets x motor direction
        if (x_dir == 1) {
          digitalWrite(x_motor_direction, HIGH);
        }
        if (x_dir == 0) {
          digitalWrite(x_motor_direction, LOW);
        }
        digitalWrite(x_motor_step, HIGH);
        delay(dl);
        digitalWrite(x_motor_step, LOW);
        delay(dl);
      }

      // Moves y motor
      for (int i = 0; i < y_steps; i++){
        //Sets y motor direction
        if (y_dir == 1) {
          digitalWrite(y_motor_direction, HIGH);
        }
        if (y_dir == 0) {
          digitalWrite(y_motor_direction, LOW);
        }
        digitalWrite(y_motor_step, HIGH);
        delay(dl);
        digitalWrite(y_motor_step, LOW);
        delay(dl);
      }

      // Moves z motor
      for (int i = 0; i < z_steps; i++){
        //Sets z motor direction
        if (z_dir == 0) {
          digitalWrite(z_motor_direction, HIGH);
        }
        if (z_dir == 1) {
          digitalWrite(z_motor_direction, LOW);
        }
        digitalWrite(z_motor_step, HIGH);
        delay(dl);
        digitalWrite(z_motor_step, LOW);
        delay(dl);
      }
      
      //Responds back to program saying is ready for next print  
      results = results + 2;
      Serial.print(results);
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
