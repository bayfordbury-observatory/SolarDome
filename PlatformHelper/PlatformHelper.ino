

// defines pins numbers
const int enPin = 4; 
const int stepPin = 3; 
const int dirPin = 2; 

const int xp = 5; 
const int xn = 6; 
const int yp = 7; 
const int yn = 8; 

String inData;
bool newMsg = false;
 
void setup() {
    
    pinMode(enPin,OUTPUT); 
    pinMode(stepPin,OUTPUT); 
    pinMode(dirPin,OUTPUT);
  
    pinMode(xp,OUTPUT); 
    pinMode(xn,OUTPUT); 
    pinMode(yp,OUTPUT); 
    pinMode(yn,OUTPUT); 
  
    digitalWrite(enPin,HIGH);
  
    Serial.begin(115200);
    while (!Serial);  // For Yun/Leo/Micro/Zero/...
   // delay(100);
    
    delay(1000);
    
}


void loop() {


      while (Serial.available() > 0){
              
      char recieved = Serial.read();
      //Serial.print(recieved);
      // Process message when new line character is recieved
      if (recieved == '\n' && newMsg){
          //Serial.print("MSG>");
          //Serial.println(inData);
          //message received, parse it
        
          if(inData[0]=='E' || inData[0]=='W' || inData[0]=='N' || inData[0]=='S'){
              String stringin(inData);
              int strLength= stringin.length();
              
              String guideTime = stringin.substring(1,strLength);
              
              uint32_t guideTimeInt = strtoul(guideTime.c_str(), NULL, 10);

              Serial.print("Moving ");
              switch (inData[0]) {
                case 'E':
                    Serial.print("East");
                    break;  
                case 'W':
                    Serial.print("West");
                    break;
                case 'N':
                    Serial.print("North");
                    break;
                case 'S':
                    Serial.print("South");
                    break;
              }
              Serial.print(" for ");
              Serial.print(guideTimeInt);
              Serial.print("ms");
              
              switch (inData[0]) {
                case 'E':
                    digitalWrite(xp, HIGH);
                    break;  
                case 'W':
                    digitalWrite(xn, HIGH);
                    break;
                case 'N':
                    digitalWrite(yp, HIGH);
                    break;
                case 'S':
                    digitalWrite(yn, HIGH);
                    break;
              }
              
              delay(guideTimeInt);

             switch (inData[0]) {
                case 'E':
                    digitalWrite(xp, LOW);
                    break;  
                case 'W':
                    digitalWrite(xn, LOW);
                    break;
                case 'N':
                    digitalWrite(yp, LOW);
                    break;
                case 'S':
                    digitalWrite(yn, LOW);
                    break;
              }
              Serial.println(" - done");
             

            }
         inData = ""; // Clear recieved buffer
         newMsg=false;

      }else if(recieved == '\r' && newMsg){
        
      }else if(newMsg){
        
          inData += recieved; 
        
      }else if(recieved == '#'){
          newMsg=true;
        
      }
      
  }
  
  //stepper stuff
     /*
       digitalWrite(enPin,LOW);
       delay(10);
      
      digitalWrite(dirPin,HIGH); // Enables the motor to move in a particular direction
      // Makes 200 pulses for making one full cycle rotation
      for(int x = 0; x < 512; x++) {
        digitalWrite(stepPin,HIGH); 
        delayMicroseconds(10000); 
        digitalWrite(stepPin,LOW); 
        delayMicroseconds(10000); 
      }
      digitalWrite(enPin,HIGH);
      delay(5000); // One second delay.
      digitalWrite(enPin,LOW);
      delay(10);
      
      digitalWrite(dirPin,LOW); //Changes the rotations direction
      // Makes 400 pulses for making two full cycle rotation
      for(int x = 0; x < 512; x++) {
        digitalWrite(stepPin,HIGH);
        delayMicroseconds(10000);
        digitalWrite(stepPin,LOW);
        delayMicroseconds(10000);
      }

      digitalWrite(enPin,HIGH);
      delay(10000);
*/
      
    }
