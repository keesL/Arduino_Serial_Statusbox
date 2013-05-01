const int LED_RED    = 2;   // digital pin
const int LED_AMBER  = 3;   // digital pin
const int LED_GREEN  = 4;   // digital pin
const int LED_STATUS = 9;   // digital pin

const char FLAG_RED   = 1;  // bit 1
const char FLAG_AMBER = 2;  // bit 2
const char FLAG_GREEN = 4;  // bit 3

// set initial states to all lights off
int RED   = LOW;
int AMBER = LOW;
int GREEN = LOW;

void setup() {
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_AMBER, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  digitalWrite(LED_STATUS, HIGH);
  Serial.begin(9600);
}

/* Test the appropriate bit to see if the corresponding
 * LED should be on or off
 * 
 * int in   -- the value to test
 * int flag -- the value to test against
 *
 * returns: HIGH if the light must be on or LOW when not
*/ 
int getLED(int in, int flag) {
  if ((in & flag) == flag) return HIGH;
  else return LOW;
}

void loop() {
  char in;

  // only do stuff if we have serial data waiting
  if (Serial.available() > 0) {
    in = Serial.parseInt();
    digitalWrite(LED_RED,   getLED(in, FLAG_RED));
    digitalWrite(LED_AMBER, getLED(in, FLAG_AMBER));
    digitalWrite(LED_GREEN, getLED(in, FLAG_GREEN));
  }
}
