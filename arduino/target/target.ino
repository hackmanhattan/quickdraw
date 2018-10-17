#include <FastLED.h>


#define NUM_LEDS 28
#define CLOCK_PIN 1
#define DATA_PIN 0
#define PIEZO_PIN A1

int threshold = 500;
int readcycle = 10;

int impact_max = 1024/8;

CRGB leds[NUM_LEDS];
void setup()
{
  pinMode(PIEZO_PIN, INPUT);
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN>(leds, NUM_LEDS);

    for(int dot = 0; dot < NUM_LEDS; dot++) { 
      leds[dot] = CRGB( 255, 0, 0);
      FastLED.show();
      leds[dot] = CRGB::Black;
    }
    delay(1000);
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
        piezo_read = min(piezo_read, impact_max);
        int tgtled = map(piezo_read, 0, impact_max, 0, NUM_LEDS);

          for(int dot = 0; dot < tgtled; dot++) { 
          leds[dot] = CRGB::Blue;
    
          } 
          for(int dot=tgtled;dot<NUM_LEDS;dot++) {
            leds[dot] = CRGB::Red;
          }

          leds[tgtled] = CRGB::Yellow;
          FastLED.show();
          if(piezo_read > (impact_max * 0.75)) {
            delay(4000);
          }

}
