
#define enable_1 2
#define step_1 3
#define dir_1 4

#define enable_2 5
#define step_2 6
#define dir_2 7

int dir = 0;
int motorSpeed = 500;
int totalRounds = 1;

void setup() {
   
  pinMode(enable_1, OUTPUT);
  pinMode(step_1, OUTPUT);
  pinMode(dir_1, OUTPUT);

  pinMode(enable_2, OUTPUT);
  pinMode(step_2, OUTPUT);
  pinMode(dir_2, OUTPUT);

  digitalWrite(enable_1, LOW);

  digitalWrite(enable_2, LOW);
}

void loop() {

  // give motors some breathing time
  // before switching direction
  delay(100);

  // set direction
  if (dir == 0) {
    digitalWrite(dir_1, LOW);
    digitalWrite(dir_2, HIGH);
  } else {
    digitalWrite(dir_1, HIGH);
    digitalWrite(dir_2, LOW);
  }

  // one full round takes 1600 pulses
  for (int rounds = 0 ; rounds < totalRounds * 1600; rounds++) {
      digitalWrite(step_1, HIGH);
      digitalWrite(step_2, HIGH);
      delayMicroseconds(motorSpeed);
      digitalWrite(step_1, LOW);
      digitalWrite(step_2, LOW);
      delayMicroseconds(motorSpeed);
  }
  
  // reverse direction for next run
  dir = 1 - dir;
}
