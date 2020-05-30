char c;
int PWMpin = 11;
float U, i, x, y;
unsigned long currentTime, previousTime;
double elapsedTime;
float error,last,cum, rate;
float sp2, sp1;
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

sp2=0;
}

void loop() {

c = Serial.read();
if((c!=57)&&(float(c)>0)) {

sp1 = float(c);
sp1=sp1-48;
}

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

if ((c == 57)&&(x>0)) {
Serial.print(x);
Serial.print(",");
Serial.println(y);
}
delay(50);

}
