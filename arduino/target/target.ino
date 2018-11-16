#include <FastLED.h>


#define NUM_LEDS 28
#define CLOCK_PIN 1
#define DATA_PIN 0
#define PIEZO_PIN A1
#define GAME_OUT A2

float threshold = 0.1;
int readcycle = 10;

int impact_max = 1024;

CRGB leds[NUM_LEDS];

void setup()
{
  pinMode(PIEZO_PIN, INPUT);
  pinMode(GAME_OUT, INPUT);
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN>(leds, NUM_LEDS);

  for(int dot = 0; dot < NUM_LEDS; dot++) { 
      leds[dot] = CRGB( 255, 0, 0);
      FastLED.show();
      leds[dot] = CRGB::Black;
  }
  

}

int getPizeoReading() {
  int sum = 0;
  for(int i=0;i<readcycle;i++) {
    sum += analogRead(PIEZO_PIN);
  }
  return sum / readcycle;
}

void loop() {
        int piezo_read = getPizeoReading();
        //piezo_read = min(piezo_read, impact_max);
        int tgtled = map(piezo_read, 0, impact_max, 0, NUM_LEDS);
        
        if(piezo_read < (impact_max * threshold)) {
          for(int dot=0;dot<NUM_LEDS;dot++) {
            leds[dot] = CRGB::Blue;
          }
          FastLED.show();
          pinMode(GAME_OUT,OUTPUT);
          analogWrite(GAME_OUT,255);
          delay(200);
          analogWrite(GAME_OUT,0);
          pinMode(GAME_OUT,INPUT);
          delay(300);
        } else {
          for(int dot = 0; dot < NUM_LEDS; dot++) { 
            leds[dot] = CRGB::Red;
          } 
          FastLED.show();     
        }
}

 
void writeToGame(int tgtInput) {
  int outputVal = map(tgtInput,0,1023,0,254);
  analogWrite(GAME_OUT,outputVal);
}
