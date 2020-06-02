//deklarácia používaných premenných
char c; // čítaná hodnota z Raspberry
int PWMpin_RC = 11; //zápis dig. pinu prveho obvodu
int PWMpin_RC_1 = 10;  //zápis dig. pinu druheho obvodu
float U_RC, U_RC_1, i, x_RC, y_RC_1; // výstupy

//premenné pre PID
unsigned long currentTime, previousTime; 
double elapsedTime;
float error,last,cum, rate;
float sp1; // požadovaná hodnota ustálenia
float output_RC,output_RC_1;
//parametre PID regulátora
float P = 13;
float I = 0.0066;
float D = 5;


//PID regulátor
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
pinMode(PWMpin_RC, OUTPUT);
pinMode(PWMpin_RC_1, OUTPUT);
Serial.begin(9600);
}

void loop() {

c = Serial.read(); // čítanie hodnoty z Raspberry
if((c!=57)&&(float(c)>0)) { //podmienka ktorou zapisujeme požadovaný výstup
sp1 = float(c);
sp1=sp1-48; //prepočet z ASCII na reálne číslo
}

//prvý RC obvod
U_RC=analogRead(A0); 
output_RC = PID(U_RC*0.004882, sp1);
if (output_RC>5){
output_RC=5;
}
if (output_RC<0){
output_RC=0;
}
analogWrite(PWMpin_RC,(output_RC)*51);
x_RC=U_RC*0.004882; //vystup prvého RC obvodu


//druhý RC obvod
U_RC_1=analogRead(A1);
output_RC_1 = PID(U_RC_1*0.004882, sp1);
if (output_RC_1>5){
output_RC_1=5;
}
if (output_RC_1<0){
output_RC_1=0;
}
analogWrite(PWMpin_RC_1,(output_RC_1)*51);
y_RC_1=U_RC_1*0.004882; //vystup prvého RC obvodu

//zápis výstupov
if ((c ==57 )&&(x_RC>0)) {
Serial.print(x_RC);
Serial.print(",");
Serial.println(y_RC_1);
}
delay(50); //oneskorenie 0.05sekundy
}
