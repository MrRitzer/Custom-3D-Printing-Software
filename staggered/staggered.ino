#define distance_x 7500
#define distance_y 26
#define distance_z 90

#define z_adjustment_long 15000
#define z_adjustment_fine 10

#define decrease_x 250

int length_x;
int start = false;
int setting = false;
int raster =8;
int layer =6;
int odd;
int dl1=1;  /*speed control here*/
int adjust_delay=1;
int wait_after_adjustment=500;

int line_num_x = raster*2;
int line_num_y = line_num_x-1;

int curr_line_num_x = 1;
int curr_line_num_y = 1;
int curr_layer = 1;

int direction_x;
int direction_y;
int direction_z;

int pos_x = 0;
int pos_y = 0;
int pos_z = 0;

int pause_tag=1;

void setup() {
  pinMode(2, INPUT);      /* stop button*/
  pinMode(3, INPUT);      /* Start button*/
  pinMode(4, OUTPUT);     /* x motor step*/
  pinMode(5, OUTPUT);     /* x motor direction*/
  pinMode(6, OUTPUT);     /* y motor step*/
  pinMode(7, OUTPUT);     /* y motor direction*/
  pinMode(8, OUTPUT);     /* z motor step*/
  pinMode(9, OUTPUT);     /* z motor direction*/
  pinMode(1, INPUT);     /* Pause button*/
  pinMode(13, INPUT);     /* Z fine down button*/
  pinMode(10, INPUT);     /* Z fine Up button*/
  pinMode(11, INPUT);     /* Z long down button*/
  pinMode(12, INPUT);      /* Z long up button*/
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
  Serial.begin(57600);


}

void loop() {
  /*Initiates process by pressing start button*/
  if (digitalRead(3)== LOW && digitalRead(2)==HIGH)
  start = true;

  /*Will enter the print if current layer number is less than max layer number, 
  Also checks the START status*/
  if (curr_layer<=layer && start==true){
     
     /*Set direction of line x*/
  if (curr_line_num_x%2 ==1) direction_x=1;
    else direction_x=2;
  
  /*Set direction of line y*/
  if (curr_layer%2 ==1) direction_y=1;
  else direction_y=2;

  /*Set direction of line x*/
  direction_z=1;

  /*starting loop for X line
  Goes into the if block if pause tag=1*/
  if (curr_line_num_x<=line_num_x && pause_tag==1) {
      
      length_x=(distance_x-(curr_layer-1)*(decrease_x*2));
      for (int x=pos_x; x<=length_x && start==true; x++){
             /*one step of x for next block of code*/
             if (direction_x==1) digitalWrite(5, HIGH);
             else digitalWrite(5, LOW);
             digitalWrite(4, HIGH);
             delay(dl1);
             digitalWrite(4, LOW);
             delay(dl1); /*one step done here*/

             /*checks wheather pause button is pressed*/
             if (digitalRead(1)==LOW){
                start= false;
                pos_x=x; 
                pause_tag=1;      
              }

             /*checks whether STOP button is pressed*/
             if (digitalRead(2)==LOW){
                start= false;
                curr_line_num_x=1; curr_line_num_y=1; curr_layer=1;
                pos_x=0; pos_y=0;
                pause_tag=1;   
              }
      }/*one line of x is done here*/
      
      
      if (start==true) {pos_x=0; pause_tag=2;}   /*when one x line is completed, resets resets position of x to zero.  As X line is complete pause tag is set to 2 */
      digitalWrite(5, LOW);         /*Actually does nothing*/
      if (start==true)curr_line_num_x++;   /*updating x line number*/
  
  }   /*finishing loop of X line*/
  
  
   /*starting loop for Y line
  Goes into the if block if pause tag=2    */

  
  if (curr_line_num_y<=line_num_y && pause_tag==2) {
      for (int y=pos_y; y<=distance_y && start==true; y++){
            if (direction_y==1) digitalWrite(7, HIGH);
            else digitalWrite(7, LOW);
            digitalWrite(6, HIGH);
            delay(dl1);
            digitalWrite(6, LOW);
            delay(dl1);
            
            if (digitalRead(1)==LOW){
                start= false;
                pos_y=y;
                pause_tag=2;       
            }          
            if (digitalRead(2)==LOW){
            start= false;
            curr_line_num_x=1; curr_line_num_y=1; curr_layer=1;
            pos_x=0; pos_y=0;
            pause_tag=1;   
            }
      }
      if (start==true) {pos_y=0; pause_tag=1;}  /*when one Y line is completed, resets resets position of Y to zero.  As Y line is complete pause tag is set to 1 */
      digitalWrite(7, LOW);
      if (start==true) curr_line_num_y++;
  }
   
  
  if (curr_layer<=layer && curr_line_num_x>line_num_x)  {
      for (int z=0; z<=distance_z && start==true; z++){
            digitalWrite(9, HIGH);
            digitalWrite(8, HIGH);
            delay(dl1);
            digitalWrite(8,LOW);
            delay(dl1);
      }
      
      digitalWrite(9,LOW);
      curr_line_num_x=1; curr_line_num_y=1;  /*sets line numbers of x and y to initial conditions*/
      curr_layer++;
      pause_tag=1;

      for (int x=0; x<=decrease_x && start==true; x++){
             direction_x=1;
             if (direction_x==1) digitalWrite(5, HIGH);
             else digitalWrite(5, LOW);
             digitalWrite(4, HIGH);
             delay(dl1);
             digitalWrite(4, LOW);
             delay(dl1); /*one step done here*/
        }
      
  }
  }
 if (curr_layer>layer) {
 start= false;
 curr_line_num_x=1; curr_line_num_y=1; curr_layer=1;
 pos_x=0; pos_y=0;
 pause_tag=1;   
              }

 /*Z adjustment here*/
 setting=false;
 if (start==false){
  if (start==false && digitalRead(13)==LOW){
    setting = true;
    for (int zfd=0; setting==true && zfd< z_adjustment_fine; zfd++){
       digitalWrite(9, HIGH);
       digitalWrite(8, HIGH);
       delay(adjust_delay);
       digitalWrite(8,LOW);
       delay(adjust_delay);

       if (digitalRead(2)==LOW) setting=false;
    }
    delay(wait_after_adjustment);
  }

  if (start==false && digitalRead(10)==LOW){
    setting = true;
    for (int zfu=0; setting==true && zfu< z_adjustment_fine; zfu++){
       digitalWrite(9, LOW);
       digitalWrite(8, HIGH);
       delay(adjust_delay);
       digitalWrite(8,LOW);
       delay(adjust_delay);

       if (digitalRead(2)==LOW) setting=false;
    }
    delay(wait_after_adjustment);
  }

  if (start==false && digitalRead(11)==LOW){
    setting = true;
    for (int zld=0; setting==true && zld< z_adjustment_long; zld++){
       digitalWrite(9, HIGH);
       digitalWrite(8, HIGH);
       delay(adjust_delay);
       digitalWrite(8,LOW);
       delay(adjust_delay);

       if (digitalRead(2)==LOW) setting=false;
    }
    delay(wait_after_adjustment);
  }

  if (start==false && digitalRead(12)==LOW){
    setting = true;
    for (int zlu=0; setting==true && zlu< z_adjustment_long; zlu++){
       digitalWrite(9, LOW);
       digitalWrite(8, HIGH);
       delay(adjust_delay);
       digitalWrite(8,LOW);
       delay(adjust_delay);

       if (digitalRead(2)==LOW) setting=false;
    }
    delay(wait_after_adjustment);
  }
 }
}
 
