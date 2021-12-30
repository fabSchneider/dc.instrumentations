#include <AccelStepper.h>

#define enable_1 2
#define step_1 3
#define dir_1 4

#define enable_2 5
#define step_2 6
#define dir_2 7

//horizontal distance between motors [mm]
int motorDist = 1200;
//length of the cable at position 0 [mm]
int homeLength = 1000;
//length difference per motor step [mm/step]
float lengthPerStep = 0.0196f;

//the motors maximum speed
int maxSpeed = 1000;

float curr_x, curr_y;
float r1, r2;

//motor speeds
float d1 = 0;
float d2 = 0;

AccelStepper m1 = AccelStepper(AccelStepper::DRIVER , step_1, dir_1);
AccelStepper m2 = AccelStepper(AccelStepper::DRIVER , step_2, dir_2);

const byte numChars = 32;
// an array to store the received data
char receivedChars[numChars]; 
String data;
const char endMarker = '\n';
const char *delimiter = " ";
boolean newData = false;
static byte ndx = 0;

float cmd_x, cmd_y;

void setup()
{
  pinMode(enable_1, OUTPUT);
  pinMode(step_1, OUTPUT);
  pinMode(dir_1, OUTPUT);

  pinMode(enable_2, OUTPUT);
  pinMode(step_2, OUTPUT);
  pinMode(dir_2, OUTPUT);

  digitalWrite(enable_1, LOW);
  digitalWrite(enable_2, LOW);

  Serial.begin(115200);
  Serial.println("<Arduino is ready>");

  // Set the maximum speed in steps per second
  m1.setMaxSpeed(maxSpeed);
  m2.setMaxSpeed(maxSpeed);
}

void loop()
{
  receiveData();

  if (newData) {
    processData();
    newData = false;
  }

  calculateCartesian();
  calculateSpeeds();

  m1.setSpeed(d1 * maxSpeed);
  m2.setSpeed(d2 * maxSpeed);

  m1.runSpeed();
  m2.runSpeed();
}

//calculates the current position of the pen 
//in cartesion coordinates with motor 1 at position x0 y0
void calculateCartesian(){

  float s1 = m1.currentPosition();
  //negate due to reversed winding direction
  float s2 = -m2.currentPosition();

  r1 = homeLength + s1 * lengthPerStep;
  r2 = homeLength + s2 * lengthPerStep;

  curr_x = (r1 * r1 - r2 * r2 + motorDist * motorDist) / (2.0f * motorDist);
  curr_y = sqrtf(r1 * r1 - curr_x * curr_x);

  Serial.println("r1 " + String(r1) + " r2 " + String(r2) + "  x" + String(curr_x) + " y" + String(curr_y));
}

void calculateSpeeds(){
  float new_r1 = sqrtf(powf(curr_x + cmd_x, 2) + powf(curr_y + cmd_y, 2));
  float new_r2 = sqrtf(powf(curr_x - motorDist + cmd_x, 2) + powf(curr_y + cmd_y, 2));

  d1 = (r1 - new_r1);
  d2 = -(r2 - new_r2);

  Serial.println("d1 " + String(d1) + " d2 " + String(d2));
}

void receiveData() {

  if (Serial.available() > 0 && newData == false) {
    char rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    }
    else {
      // terminate the string
      receivedChars[ndx] = '\0'; 
      ndx = 0;
      newData = true;
    }
  }
}

bool processData() {
  data = strtok(receivedChars, delimiter);

  //read x
  if (data == NULL) {
    return false;
  }

  float tx = data.toFloat();

  //read y
  data = strtok(NULL, delimiter);
  if (data == NULL) {
    return false;
  }

  float ty = data.toFloat();

  cmd_x = tx;
  cmd_y = ty;
  return true;
}