#define ENCODER_OPTIMIZE_INTERRUPTS
#include <Encoder.h>


int incomingByte = 0;   // for incoming serial data


/*
 * Pins available 
 * 
 * 0, 1, 2, 3, 7  interrupts
 * 4, 8, 12
 * (3), 5, 6, 9, 10, 11, 13 PWM 
 * 
 * A0-A5 (digital 18-23)
 * 
 * 14, 15, 16 on ICSP
 * 
 * 3x Gnd, 3.3v, 5v
 */

#define shutterIN1 5
#define shutterIN2 6
#define shutterSD 9

#define shutterEncA 0
#define shutterEncB 1
#define shutterEncI 4

#define rotationIN1 11
#define rotationIN2 13
#define rotationSD 10

#define rotationEncA 2
#define rotationEncB 3
#define rotationEncI 7

#define shutterOpened 8
#define shutterClosed 12

#define rotationHome 23

#define buttonOpen 22
#define buttonClose 21
#define buttonLeft 20
#define buttonRight 19

#define relayPSU 18

int shutterSpeed = 0;
int rotationSpeed = 0;
int i;

int maxShutterSpeed=200;
int maxRotationSpeed=200;

int rotationAccel = 4;
int shutterAccel = 4;

long rotationPos = 0;
long shutterPos = 0;

   Encoder rotationEnc(rotationEncA, rotationEncB); 
   Encoder shutterEnc(shutterEncA, shutterEncB); 

void setup() {
  // put your setup code here, to run once:


//----- PWM frequency for D9 & D10 -----
//Timer1 divisor = 2, 16, 128, 512, 2048
//TCCR1B = TCCR1B & B11111000 | B00000001;    // 31KHz
//TCCR1B = TCCR1B & B11111000 | B00000010;    // 3921.16 Hz
TCCR1B = TCCR1B & B11111000 | B00000011;    // 490Hz (default)
//TCCR1B = TCCR1B & B11111000 | B00000100;    // 122.5Hz
//TCCR1B = TCCR1B & B11111000 | B00000101;    // 30.6Hz
 

 
   Serial.begin(9600);

   pinMode(shutterIN1, OUTPUT);
   pinMode(shutterIN2, OUTPUT);
   pinMode(shutterSD, OUTPUT);

   pinMode(shutterEncA, INPUT);
   pinMode(shutterEncB, INPUT);
   pinMode(shutterEncI, INPUT);

   pinMode(rotationIN1, OUTPUT);
   pinMode(rotationIN2, OUTPUT);
   pinMode(rotationSD, OUTPUT);

   pinMode(rotationEncA, INPUT);
   pinMode(rotationEncB, INPUT);
   pinMode(rotationEncI, INPUT);

   pinMode(shutterOpen, INPUT_PULLUP);
   pinMode(shutterClosed, INPUT_PULLUP);

   pinMode(rotationHome, INPUT_PULLUP);

   pinMode(buttonOpen, INPUT_PULLUP);
   pinMode(buttonClose, INPUT_PULLUP);
   pinMode(buttonLeft, INPUT_PULLUP);
   pinMode(buttonRight, INPUT_PULLUP);

   pinMode(relayPSU, OUTPUT);   
   
   analogWrite(rotationSD, 0);
   analogWrite(shutterSD, 0);

   digitalWrite(shutterIN1, LOW);
   digitalWrite(shutterIN2, LOW);

   digitalWrite(rotationIN1, LOW);
   digitalWrite(rotationIN2, LOW);




   
}



void shutterStop(){
  while(shutterSpeed>0){
      shutterSpeed--;
      analogWrite(shutterSD, shutterSpeed);
      Serial.println(shutterSpeed);
      delay(1);
  }

  digitalWrite(shutterIN1, 0);
  digitalWrite(shutterIN2, 0);
  
}

void shutterOpen(){

  digitalWrite(shutterIN1, 1);
  digitalWrite(shutterIN2, 0);

  while(shutterSpeed<maxShutterSpeed){
      shutterSpeed++;
      analogWrite(shutterSD, shutterSpeed);
      Serial.println(shutterSpeed);
      delay(shutterAccel);
  }
  
}


void shutterClose(){
  
  digitalWrite(shutterIN1, 0);
  digitalWrite(shutterIN2, 1);

  while(shutterSpeed<maxShutterSpeed){
      shutterSpeed++;
      analogWrite(shutterSD, shutterSpeed);
      Serial.println(shutterSpeed);
      delay(shutterAccel);
  }
  
}

void rotationStop(){
    while(rotationSpeed>0){
      rotationSpeed--;
      analogWrite(rotationSD, rotationSpeed);
      Serial.println(rotationSpeed);
      delay(1);
  }

  digitalWrite(rotationIN1, 0);
  digitalWrite(rotationIN2, 0);
  
  
}



void rotationLeft(){
  digitalWrite(rotationIN1, 0);
  digitalWrite(rotationIN2, 1);

  while(rotationSpeed<maxRotationSpeed){
      rotationSpeed++;
      analogWrite(rotationSD, rotationSpeed);
      Serial.println(rotationSpeed);
      delay(rotationAccel);
  }
  
}

void rotationRight(){
  digitalWrite(rotationIN1, 1);
  digitalWrite(rotationIN2, 0);

  while(rotationSpeed<maxRotationSpeed){
      rotationSpeed++;
      analogWrite(rotationSD, rotationSpeed);
      Serial.println(rotationSpeed);
      delay(rotationAccel);
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:

 rotationPos = rotationEnc.read(); 
  shutterPos = shutterEnc.read(); 


     if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
    
    
    
        if(incomingByte=='O'){
           shutterOpen();

        }else if(incomingByte=='C'){
            shutterClose();
           
        }else if(incomingByte=='S'){
            shutterStop();
           rotationStop();

        }else if(incomingByte=='L'){
            rotationLeft();
           
        }else if(incomingByte=='R'){
             rotationRight();
        }else if(incomingByte=='G'){
             Serial.println(rotationPos);
             Serial.println(shutterPos);
          
        }
     }
}
