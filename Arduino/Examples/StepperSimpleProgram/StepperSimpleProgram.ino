#define enable_1 2
#define step_1 3
#define dir_1 4

#define enable_2 5
#define step_2 6
#define dir_2 7

int dir = 0;

void setup() {
  pinMode(enable_2, OUTPUT);
  pinMode(step_2, OUTPUT);
  pinMode(dir_2, OUTPUT);

  // enable motor 2
  digitalWrite(enable_2, LOW);
}

void loop() {

  // give motors some breathing time
  // before switching direction
  delay(2);

  // set direction
  if (dir == 0) {
    digitalWrite(dir_2, LOW);
  } else {
    digitalWrite(dir_2, HIGH);
  }

  int totalRounds = 2;
  // one full round takes 1600 pulses
  for (int rounds = 0 ; rounds < totalRounds * 1600; rounds++) {
      digitalWrite(step_2, HIGH);
      delayMicroseconds(500);
      digitalWrite(step_2, LOW);
      delayMicroseconds(500);
  }
  
  // reverse direction for next run
  dir = 1 - dir;
}
