// This routine can be used to measure the cable displacement in mm per step
// On start motor 1 will move for 10000 steps
// The resulting length difference of the belt divided by the steps gives us the mm per step ratio

const uint8_t M1_EN = 2;
const uint8_t M1_STEP = 3;
const uint8_t M1_DIR = 4;

const uint8_t M2_EN = 5;
const uint8_t M2_STEP = 6;
const uint8_t M2_DIR = 7;

int interval = 1000;

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

  for(int i = 0; i < 10000; i++){
    digitalWrite(M1_STEP, LOW);
    delayMicroseconds(interval);
    digitalWrite(M1_STEP, HIGH);
    delayMicroseconds(interval);
  }
}


void loop()
{

}