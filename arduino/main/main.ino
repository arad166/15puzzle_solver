#include <VarSpeedServo.h>       // ライブラリのインクルード
VarSpeedServo xservo;           // サーボオブジェクトの作成
VarSpeedServo yservo0;
VarSpeedServo yservo1;
 
const int xservo_pin = 11;         // サーボ接続ピン
const int yservo0_pin = 10;
const int yservo1_pin = 9;
 
void setup(){
  Serial.begin(9600);
  xservo.attach(xservo_pin);
  yservo0.attach(yservo0_pin);
  yservo1.attach(yservo1_pin);
} 
 
void loop() {
  if(Serial.available()){
    String data = Serial.readStringUntil('\n');
    int x, y0, y1;
    if (sscanf(data.c_str(), "%d,%d,%d", &x, &y0, &y1) == 3) {
        xservo.write(x,60);
        yservo0.write(y0,40);
        yservo1.write(y1,40);
        int x = xservo.read();
        int y0 = yservo0.read();
        int y1 = yservo1.read();
        Serial.print("x: ");
        Serial.print(x);
        Serial.print(", y0: ");
        Serial.print(y0);
        Serial.print(", y1: ");
        Serial.println(y1);
    }
  }
}