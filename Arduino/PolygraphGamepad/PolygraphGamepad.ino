#include <AccelStepper.h>

const uint8_t M1_EN = 2;
const uint8_t M1_STEP = 3;
const uint8_t M1_DIR = 4;

const uint8_t M2_EN = 5;
const uint8_t M2_STEP = 6;
const uint8_t M2_DIR = 7;

//horizontal distance between motors [mm]
const float MOTOR_DIST = 2000;
const float MOTOR_DIST_SQ = MOTOR_DIST * MOTOR_DIST;

//length of the cable at position 0 [mm]
const float HOME_LEN = 1500;
//cable length difference per motor step [mm/step]
const float LEN_PER_STEP = 0.0196f;

//the motors maximum speed
int maxSpeed = 3200;

float curr_x, curr_y;
float curr_r1, curr_r2;

//motor speed delta
float d1 = 0.0f;
float d2 = 0.0f;

AccelStepper m1 = AccelStepper(AccelStepper::DRIVER, M1_STEP, M1_DIR);
AccelStepper m2 = AccelStepper(AccelStepper::DRIVER, M2_STEP, M2_DIR);

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
  pinMode(M1_EN, OUTPUT);
  pinMode(M1_STEP, OUTPUT);
  pinMode(M1_DIR, OUTPUT);

  pinMode(M2_EN, OUTPUT);
  pinMode(M2_STEP, OUTPUT);
  pinMode(M2_DIR, OUTPUT);

  digitalWrite(M1_EN, LOW);
  digitalWrite(M2_EN, LOW);

  Serial.begin(115200);
  Serial.println("<Arduino is ready>");

  // Set the maximum speed in steps per second
  m1.setMaxSpeed(maxSpeed);
  m2.setMaxSpeed(maxSpeed);
}

void loop()
{
  if (receiveData())
  {
    processData();
    calculateCartesian();
    calculateSpeeds();
    updateSpeeds();
    dump();
  }

  m1.runSpeed();
  m2.runSpeed();
}

//calculates the current position of the pen
//in cartesian coordinates with motor 1 at position x0 y0
void calculateCartesian()
{
  float p1 = m1.currentPosition();
  //negate due to reversed winding direction
  float p2 = -m2.currentPosition();

  //convert to radii
  curr_r1 = p1 * LEN_PER_STEP + HOME_LEN;
  curr_r2 = p2 * LEN_PER_STEP + HOME_LEN;

  //calculate x and y as the intersection point of the two circles with r1 and r2
  curr_x = (curr_r1 * curr_r1 - curr_r2 * curr_r2 + MOTOR_DIST_SQ) / (2.0f * MOTOR_DIST);
  curr_y = sqrtf(curr_r1 * curr_r1 - curr_x * curr_x);
}

void calculateSpeeds()
{

  float target_x = curr_x + cmd_x;
  float target_y = curr_y + cmd_y;

  //calculate the target radius for m1 and m2
  float target_r1 = length(target_x, target_y);
  float target_r2 = length(target_x - MOTOR_DIST, target_y);

  //calculate the difference between the current and target radius
  float r1_d = target_r1 - curr_r1;
  float r2_d = curr_r2 - target_r2;

  clampToUnit(r1_d, r2_d);
  d1 = r1_d;
  d2 = r2_d;
}

//updates the motor speeds
void updateSpeeds()
{
  m1.setSpeed(d1 * maxSpeed);
  m2.setSpeed(d2 * maxSpeed);
}

//returns the length of a 2d vector
float length(float x, float y)
{
  return sqrtf(x * x + y * y);
}

//Makes sure that a 2d vector is contained within the unit circle
void clampToUnit(float &x, float &y){
  float mag = length(x, y);
  if (mag > 0.001f)
  {
    x = x / mag * min(mag, 1.0f);
    y = y / mag * min(mag, 1.0f);
  }
  else
  {
    x = 0.0f;
    y = 0.0f;
  }
}

//stores incoming data in receivedChars array
//returns true if new data is available
bool receiveData()
{
  if (Serial.available() > 0 && newData == false)
  {
    char rc = Serial.read();

    if (rc != endMarker)
    {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars)
      {
        ndx = numChars - 1;
      }
    }
    else
    {
      // terminate the string
      receivedChars[ndx] = '\0';
      ndx = 0;
      return true;
    }
  }
  return false;
}

bool processData()
{
  data = strtok(receivedChars, delimiter);

  //read x
  if (data == NULL)
  {
    return false;
  }

  float tx = data.toFloat();

  //read y
  data = strtok(NULL, delimiter);
  if (data == NULL)
  {
    return false;
  }

  float ty = data.toFloat();

  cmd_x = tx;
  cmd_y = ty;
  return true;
}

//prints the current state to the serial
void dump()
{
  Serial.println("r1 " + String(curr_r1) + " r2 " + String(curr_r2) + " | x" + String(curr_x) + " y" + String(curr_y) + " | d1 " + String(d1) + " d2 " + String(d2));
}