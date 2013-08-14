#include <Wire.h>

#include <Servo.h> 
#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;
 
Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
 
void setup() 
{ 
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
   pinMode(13, OUTPUT);
    Serial.begin(9600);         // start serial for output
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);
    myservo.write(30);
    Serial.println("Ready!");
}

void loop() {
    delay(100); // waits 100ms for the servo to reach the position 
} 

// callback for received data
void receiveData(int byteCount){

    while(Wire.available()) {
        number = Wire.read();
        Serial.print("data received: ");
        Serial.println(number);

        if (number == 1){

            if (state == 0){
                digitalWrite(13, HIGH); // set the LED on
                state = 1;
                myservo.write(1);
            }
            else{
                digitalWrite(13, LOW); // set the LED off
                state = 0;
                myservo.write(1);
            }
        }
        else{
        myservo.write(number);
        }
     }
}

// callback for sending data
void sendData(){
    Wire.write(number);
}

