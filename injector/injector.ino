int pinA = 6; //Down 
int pinB = 7; //Up 

void setup(){
 pinMode(pinA, OUTPUT);
 pinMode(pinB, OUTPUT);

}

void loop(){
    digitalWrite(pinB,HIGH);
    delay(10000);
    digitalWrite(pinB,LOW);
    delay(2000);
}