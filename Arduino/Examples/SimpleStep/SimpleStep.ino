#define enable_1 2
#define step_1 3
#define dir_1 4

#define enable_2 5
#define step_2 6
#define dir_2 7

void setup() {
  pinMode(enable_2, OUTPUT);
  pinMode(step_2, OUTPUT);
  pinMode(dir_2, OUTPUT);

  digitalWrite(enable_2, LOW);
  digitalWrite(dir_2, LOW);
}

void loop() {
  digitalWrite(step_2,HIGH);
  delay(1); 
  digitalWrite(step_2,LOW);
  delay(1);
}
