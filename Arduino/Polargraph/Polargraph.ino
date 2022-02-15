#include <AccelStepper.h>

//#define SEND_RESPONSE

const int CMD_DIR = 0;
const int CMD_POS = 1;
const int CMD_FEED = 2;

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
const float LEN_PER_STEP = 0.035f;

const int LIMIT_MIN_X = -800;
const int LIMIT_MAX_X = 1000;
const int LIMIT_MIN_Y = -550;
const int LIMIT_MAX_Y = 800;

float home_x;
float home_y;

//the motors maximum speed
int maxSpeed = 3200;
int speed = maxSpeed;

//machine x, y position
float m_x, m_y;

bool movePosition = false;
float reached_epsilon = 0.1f;

//converts machine x to work x
float toWorkX(float x){
  return x - home_x;
}

//converts machine y to work y
float toWorkY(float y){
  return y - home_y;
}

//converts work x to machine x
float toMachineX(float x){
  return x + home_x;
}

//converts work y to machine y
float toMachineY(float y){
  return y + home_y;
}

float curr_r1, curr_r2;

//motor speed delta
float d1 = 0.0f;
float d2 = 0.0f;

//looking front onto the polargraph, m1 is left and m2 is right
AccelStepper m1 = AccelStepper(AccelStepper::DRIVER, M1_STEP, M1_DIR);
AccelStepper m2 = AccelStepper(AccelStepper::DRIVER, M2_STEP, M2_DIR);

const byte numChars = 64;
// an array to store the received data
char receivedChars[numChars];
String data;
const char endMarker = '\n';
const char *delimiter = " ";
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

  //Calclate home pos
  calculateIntersection(HOME_LEN, HOME_LEN, home_x, home_y);
}

void loop()
{
  if (receiveData())
  {
    processData();
    calculateCartesian();
    calculateSpeeds();
    updateSpeeds();
    #ifdef SEND_RESPONSE
    dump();
    #endif
  }
  else
  {
    calculateCartesian();
    calculateSpeeds();
    updateSpeeds();
    checkReachedPosition();
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
  float x, y;
  calculateIntersection(curr_r1, curr_r2, x, y);
  m_x = x;
  m_y = y;
}

//calculate x and y as the intersection point of the two circles with r1 and r2
void calculateIntersection(const float r1, const float r2, float& x, float& y){
  x = (r1 * r1 - r2 * r2 + MOTOR_DIST_SQ) / (2.0f * MOTOR_DIST);
  y = -sqrtf(r1 * r1 - x * x);
}

void calculateSpeeds()
{
  float target_x;
  float target_y;

  //when movePosition flag is true
  //treat the current cmd coordinates as the target
  if(movePosition){
    target_x = toMachineX(cmd_x);
    target_y = toMachineY(cmd_y);
  }
  //otherwise add the cmd coordinates 
  // to current machine position
  else{
    target_x = m_x + cmd_x;
    target_y = m_y + cmd_y;
  }

  //keep target within limits
  target_x = toMachineX(clamp(LIMIT_MIN_X, LIMIT_MAX_X, toWorkX(target_x)));
  target_y = toMachineY(clamp(LIMIT_MIN_Y, LIMIT_MAX_Y, toWorkY(target_y)));

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

void checkReachedPosition(){
  if(movePosition){
    if(lengthSQ(d1, d2) < reached_epsilon){
      movePosition = false;    
      cmd_x = 0;
      cmd_y = 0;
      Serial.println('r');
    }
  }
}

//updates the motor speeds
void updateSpeeds()
{
  m1.setSpeed(d1 * speed);
  m2.setSpeed(d2 * speed);
}

//returns the length of a 2d vector
float length(float x, float y)
{
  return sqrtf(x * x + y * y);
}

//returns the length of a 2d vector
float lengthSQ(float x, float y)
{
  return x * x + y * y;
}

//clamps a value in between a minimum and a maximum
float clamp(float _min, float _max, float value)
{
  return max(_min, min(_max, value));
}

//Makes sure that a 2d vector is contained within the unit circle
void clampToUnit(float &x, float &y)
{
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
  if (Serial.available() > 0)
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

  if (data == NULL){
     return false;
  }

  int tp = data.toInt();
  float tx = 0;
  float ty = 0;

  switch (tp)
  {
  case CMD_DIR: 

    //read x
    data = strtok(NULL, delimiter);
    if (data == NULL)
    {
      return false;
    }

    tx = data.toFloat();

    //read y
    data = strtok(NULL, delimiter);
    if (data == NULL)
    {
      return false;
    }
    ty = data.toFloat();
    cmd_x = tx;
    cmd_y = ty;
    movePosition = false;
    return true;
  case CMD_POS:

    //read x
    data = strtok(NULL, delimiter);
    if (data == NULL)
    {
      return false;
    }

    tx = data.toFloat();

    //read y
    data = strtok(NULL, delimiter);
    if (data == NULL)
    {
      return false;
    }
    ty = data.toFloat();
    cmd_x = tx;
    cmd_y = ty;
    movePosition = true;
    return true;
  case CMD_FEED:
  {
    //read feed
    data = strtok(NULL, delimiter);
    if (data == NULL)
    {
      return false;
    }
    int feed = data.toInt();
    speed = feed;
    return true;
  } 
  default:
    return false;
  }
}

//prints the current state to the serial
void dump()
{
  String moveType;
  if(movePosition){
    moveType = "POS";
  }else{
    moveType = "DIR";
  }

  Serial.println("r1 " + String(curr_r1) + " r2 " + String(curr_r2) + 
  " | x" + String(toWorkX(m_x)) + " y" + String(toWorkY(m_y)) + 
  " | d1 " + String(d1) + " d2 " + String(d2) +
  " | Move: " + moveType);
}