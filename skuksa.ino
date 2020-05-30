int PWMpin = 11;
float U, i, x, y;
unsigned long currentTime, previousTime;
double elapsedTime;
float error,last,cum, rate;
float sp1, sp2; 
float output;
float P = 13;
float I = 0.0066;
float D = 5;


float PID(float inp,float Setpoint){     
        currentTime = millis();                
        elapsedTime = (double)(currentTime - previousTime);        
        error = Setpoint - inp;                               
        cum += error * elapsedTime;                
        rate = (error - last)/elapsedTime;   
        float out = P*error + I*cum + D*rate;                        
        last = error;                                
        previousTime = currentTime;
        return out;        
}

void setup() {
  pinMode(PWMpin, OUTPUT);
  Serial.begin(9600);
  sp1=4;
  sp2=1;
}

void loop() {


  for (i=0;i<150;i++){
    U=analogRead(A0);
    output = PID(U*0.004882, sp1);
    if (output>5){
     output=5;
    }
    if (output<0){
     output=0;
    }
    analogWrite(PWMpin,(output)*51);
	x=U*0.004882;
	y=U*0.0088;
    Serial.print(x);
	Serial.print(",");
	Serial.println(y);
    delay(150);
  }
  
  for (i=0;i<150;i++){
    U=analogRead(A0);
    output = PID(U*0.004882, sp2);
    if (output>5){
     output=5; 
    }
    if (output<0){
     output=0;
    }
    analogWrite(PWMpin,(output)*51);
    x=U*0.004882;
	y=U*0.0088;
    Serial.print(x);
	Serial.print(",");
	Serial.println(y);
    delay(150);
  }
}