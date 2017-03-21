#include <NewPing.h>
#include <Roomba.h>
#include <VarSpeedServo.h>

char input;
int Servo1, Servo2, Servo3, Servo4, Servo5, distance = 0;
int PreviousAngle2 = 1681, PreviousAngle3 = 1269, PreviousAngle4 = 1064, MaxSpeed = 20;
int RangeAngle1, RangeAngle2, RangeAngle3, RangeAngle4, NewAngle2, NewAngle3, NewAngle4, MaxRange;
int Speed1, Speed2, Speed3, Speed4, PingReading = 0;
int  x = 0, EncoderDistance = 0;//Romba Distance Travelled
char Servo2_string[5], Servo3_string[5], Servo4_string[5];
bool ret;
uint8_t buf[52];
//Wireless Communication
char XCoord, YCoord, BallCol;


//Motor Speed
int Speed=200;

NewPing sonar(8, 9, 70);//Trigger Echo
NewPing Forwardsonar(10, 11, 500);//Trigger Echo
Roomba roomba(&Serial1);

VarSpeedServo myservo1;
VarSpeedServo myservo2;
VarSpeedServo myservo3;
VarSpeedServo myservo4;
VarSpeedServo myservo5;

void setup() {
  roomba.start();
  roomba.fullMode();
  Serial.begin(57600);
  Serial2.begin(115200);
  Serial3.begin(9600);
}

void loop() {

  while (Serial3.available() != 0) {
    switch (Serial3.read()) {

      //Servo Commands
      case 'a':
        myservo1.attach(2);
        myservo2.attach(3);
        myservo3.attach(4);
        myservo4.attach(5);
        myservo5.attach(6);
        myservo1.write(1475, 150, false);
        myservo2.write(PreviousAngle2, 150, false);
        myservo3.write(PreviousAngle3, 150, false);
        myservo4.write(PreviousAngle4, 150, false);
        myservo5.write(0, 50, true);
        break;

      case '1':
        Serial.println("Servo1 Scanning");
        for (int ScanPosition = 30; ScanPosition <= 150; ScanPosition++) {
          myservo1.write(ScanPosition, 255, false);
          delay(250);
          if (Serial3.available() > 0) {
            Servo1 = Serial3.read();
            if (Servo1 == '0') {
              Serial.println("Servo1 Stopped Scanning");
              break;
            }
          }
        }
        break;

      case '2':
        while (Serial3.available() == 0) {}
        for (int i = 0; i < 4; i++) {
          Servo2_string [i] = Serial3.read();
          delay(10);
        }
        Servo2 = atoi(Servo2_string) - 1000;
        Serial.print("Servo2:");
        Serial.println(Servo2);
        break;

      case '3':
        while (Serial3.available() == 0) {}
        for (int i = 0; i < 4; i++) {
          Servo3_string [i] = Serial3.read();
          delay(10);
        }
        Servo3 = atoi(Servo3_string) - 1000;
        Serial.print("Servo3:");
        Serial.println(Servo3);
        break;

      case '4':
        while (Serial3.available() == 0) {}
        for (int i = 0; i < 4; i++) {
          Servo4_string [i] = Serial3.read();
          delay(10);
        }
        Servo4 = atoi(Servo4_string) - 1000;
        Serial.print("Servo4:");
        Serial.println(Servo4);
        break;

      case 's'://Write Servo COnfiguration
        Serial.println("Actuating Motors!");
        NewAngle2 = Servo2 - 103;
        NewAngle3 = Servo3;
        NewAngle4 = 2950 - Servo4 - 103;
        RangeAngle2 = abs(NewAngle2 - PreviousAngle2);
        RangeAngle3 = abs(NewAngle3 - PreviousAngle3);
        RangeAngle4 = abs(NewAngle4 - PreviousAngle4);
        MaxRange = FindMax(RangeAngle1, RangeAngle2, RangeAngle3);
        Speed2 = round(((RangeAngle2 * 1.0) / MaxRange) * MaxSpeed);
        Speed3 = round(((RangeAngle3 * 1.0) / MaxRange) * MaxSpeed);
        Speed4 = round(((RangeAngle4 * 1.0) / MaxRange) * MaxSpeed);
        myservo2.write(NewAngle2, zerotoone(Speed2), false); //Minus 10 degree of Angle1
        myservo3.write(NewAngle3, zerotoone(Speed3), false); //Angle 2 Intact
        myservo4.write(NewAngle4, zerotoone(Speed4), true); //180-Angle-10degrees
        delay(500);
        PreviousAngle2 = NewAngle2;
        PreviousAngle3 = NewAngle3;
        PreviousAngle4 = NewAngle4;
        break;

      case 'd'://Bring Back Servo 1 to center Position and detach servos
        myservo1.write(1475, 50, true);
        myservo1.detach();
        myservo2.detach();
        myservo3.detach();
        myservo4.detach();
        myservo5.detach();
        break;

      case '5':
        while (Serial3.available() == 0) {}
        Servo5 = Serial3.read();
        if (Servo5 == '1') {
          Serial.println("Servo5 Open");
          myservo5.write(60, 50, false);
        }
        else {
          Serial.println("Servo5 Close");
          myservo5.write(0, 50, false);
        }
        break;

      //Get Ultrasonic Distance
      case 'x':
        for (int i = 0; i < 20; i++) { //20 Samples
          while (PingReading == 0) { //Do not include values of 0
            PingReading = sonar.ping_cm();
            delay(50);
          }
          distance += PingReading;
          PingReading = 0;
          delay(50);
        }
        distance = round(distance * 0.5); //*(Samples/20)*10
        Serial.print("Ping: ");
        Serial.print(distance); // Send ping, get distance in cm and print result (0 = outside set distance range)
        Serial.println("mm");
        Serial3.println(distance);
        distance = 0;
        break;

      //IRobot Commands
      case 'v':
        while (Serial3.available() == 0) {}
        EncoderDistance = Serial3.read();
        if (EncoderDistance == '3') {
          EncoderDistance = 330;

        }
        else {
          EncoderDistance = 469;
        }
        Serial.print("EncoderDistance:");
        Serial.println(EncoderDistance);
        break;

      case 'f':
        Serial.println("Forward");
        roomba.driveDirect(Speed , Speed);
        roomba.driveDirect(Speed , Speed);
        roomba.waitDistance(EncoderDistance);
        RoombaWait();
        break;
      case 'b':
        Serial.println("Backward");
        roomba.driveDirect(-Speed, -Speed);
        roomba.waitDistance(-330);
        RoombaWait();
        break;
      case 'r':
        Serial.println("Right 45 Degrees");
        roomba.driveDirect(Speed, -Speed);
        roomba.waitAngle(-45);
        RoombaWait();
        break;
      case 'e':
        Serial.println("Right 90 Degrees");
        roomba.driveDirect(Speed, -Speed);
        roomba.waitAngle(-90);
        RoombaWait();
        break;
      case 'l':
        Serial.println("Left 45 Degrees");
        roomba.driveDirect(-Speed , Speed);
        roomba.waitAngle(45);
        RoombaWait();
        break;
      case 'k':
        Serial.println("Left 90 Degrees");
        roomba.driveDirect(-Speed , Speed);
        roomba.waitAngle(90);
        RoombaWait();
        break;
      case 't':
        Serial.println("Turning");
        roomba.driveDirect(-Speed, Speed);
        roomba.waitAngle(180);
        RoombaWait();
        break;
        
      case 'o'://Ultrasonic Readings
        while (PingReading == 0) { //Do not include values of 0
          PingReading = Forwardsonar.ping_cm();
          delay(50);
        }
        Serial.print(" Forward Ping:");
        Serial.print(PingReading);
        Serial.println("cm");
        Serial3.println(PingReading);
        PingReading = 0;
        break;

      //Wireless Communication
      case 'w':
        while (Serial2.available() == 0) {};
        XCoord = Serial2.read();
        while (Serial2.available() == 0) {};
        YCoord = Serial2.read();
        while (Serial2.available() == 0) {};
        BallCol = Serial2.read();
        Serial.print("X:");
        Serial.println(XCoord);
        Serial3.println(XCoord);
        Serial.print("Y:");
        Serial.println(YCoord);
        Serial3.println(YCoord);
        Serial.print("C:");
        Serial.println(BallCol);
        Serial3.println(BallCol);
        break;

      default:
        Serial.println("Stop");
        roomba.driveDirect(0, 0);
        break;
    }
  }
}

//Function for Computing maxRange
int FindMax(int a, int b, int c) {
  int maxguess;
  maxguess = max(a, b); // biggest of A and B
  maxguess = max(maxguess, c);  // but maybe C is bigger?
  return (maxguess);
}

int BitShiftCombine( unsigned char x_high, unsigned char x_low)
{
  int combined;
  combined = x_high;              //send x_high to rightmost 8 bits
  combined = combined << 8;       //shift x_high over to leftmost 8 bits
  combined |= x_low;                 //logical OR keeps x_high intact in combined and fills in rightmost 8 bits
  return combined;

}
int zerotoone(int a) {
  if (a == 0) {
    a = 1;
  }
  else {
    a = a;
  }
  return a;
}

void RoombaWait() {
  while (x == 0 ) {
    buf[52];
    ret = roomba.getSensors(6 , buf , 52);
    x = BitShiftCombine(buf[12], buf[13]);        // Value sent as 16 bit signed value high byte first.
  }
  Serial.println(x);
  x = 0;
  ret = 0;
  Serial3.println("n");
}



