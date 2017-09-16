#include <SPI.h>
#include "TMC26XStepper.h"

int PUL=9; //define Pulse pin
int DIR=8; //define Direction pin
int ENA=7; //define Enable Pin
int xFactor = 1;
int yFactor = 4;
int stepsPerRot = 400;
//we have a stepper motor with 200 steps per rotation, CS pin 2, dir pin 6, step pin 7 and a current of 800mA
TMC26XStepper tmc26XStepper = TMC26XStepper(stepsPerRot,6,4,5,1700);
int curr_step;
int speed =  0;
int speedDirection = 100;
int maxSpeed = 1000;
int maxStepsAtATime = 800;
String cmd;

void setup() {
  pinMode (PUL, OUTPUT);
  pinMode (DIR, OUTPUT);
  pinMode (ENA, OUTPUT);

  Serial.begin(9600);
  Serial.println("==============================");
  Serial.println("TMC26X Stepper Driver Demo App");
  Serial.println("==============================");
  //set this according to you stepper
  Serial.println("Configuring stepper driver");
  //char constant_off_time, char blank_time, char hysteresis_start, char hysteresis_end, char hysteresis_decrement
  tmc26XStepper.setSpreadCycleChopper(2,24,8,6,0);
  tmc26XStepper.setRandomOffTime(0);
  tmc26XStepper.SPI_setCoilCurrent(100);
  tmc26XStepper.setMicrosteps(128);
  tmc26XStepper.setStallGuardThreshold(4,0);

  Serial.println("config finished, starting");
  Serial.println("started");
}

void step(int rpm,int steps,int dir){
  int delay = round(60.0/rpm/yFactor/stepsPerRot/2*1e6);
  Serial.println("steps = " + String(steps) + " dir = " + String(dir));
  for (int i=0; i<steps; i++)   //Backward 5000 steps
    {
      if(dir > 0) {
        digitalWrite(DIR,HIGH);
      }
      else {
        digitalWrite(DIR,LOW);
      }  
      digitalWrite(ENA,HIGH);
      
      digitalWrite(PUL,HIGH);
      delayMicroseconds(delay);
      digitalWrite(PUL,LOW);
      delayMicroseconds(delay);
    }
}

void loop() {

  if(Serial.available()) {
            cmd = Serial.readString();
            int commaIndex = cmd.indexOf(',');
            int secondCommaIndex = cmd.indexOf(',',commaIndex+1);
            int thirdCommaIndex = cmd.indexOf(',',secondCommaIndex+1);

            //  Search for the next comma just after the first
            String firstValue = cmd.substring(0, commaIndex);
            String secondValue = cmd.substring(commaIndex + 1,secondCommaIndex);
            String thirdValue = cmd.substring(secondCommaIndex+1,thirdCommaIndex);
            String fourthValue = cmd.substring(thirdCommaIndex+1);


            int xSpeed = firstValue.toInt();
            int xSteps = secondValue.toInt();
            int ySpeed = thirdValue.toInt();
            int ySteps = fourthValue.toInt();

            int xSign = xSteps/abs(xSteps);
            int ySign = ySteps/abs(ySteps);
            
            int numReps = max(abs(xSteps),abs(ySteps))/maxStepsAtATime;
            
            for (int i = 0; i < numReps; i++) {
              Serial.println("setting RPM " + firstValue + "  xstep " + secondValue + " yrpm " + thirdValue + " ystep " + fourthValue);
              tmc26XStepper.SPI_setSpeed(xSpeed);    //Set speed at 80 RPM 
              
              if(ySteps == 0) {
                
              }
              else if(i*maxStepsAtATime <= abs(ySteps)) {
                step(ySpeed,maxStepsAtATime*yFactor,ySign);
              }
              else {
                step(ySpeed,(ySteps%maxStepsAtATime)*yFactor,ySign);
              }

              if(xSteps == 0) {
                
              }
              if(i*maxStepsAtATime <= abs(xSteps)) {
                 tmc26XStepper.SPI_step(maxStepsAtATime*xFactor*xSign);
              }
              else {
                 tmc26XStepper.SPI_step((xSteps%xFactor)*xFactor*xSign);
              }
              tmc26XStepper.spi_start();         //start stepper 
              Serial.println("MOVED RPM " + firstValue + "  xstep " + secondValue + " yrpm " + thirdValue + " ystep " + fourthValue);

            }
            
  }//delay 2s
}



