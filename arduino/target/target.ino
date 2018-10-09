#include <FastLED.h>


#define NUM_LEDS 60
#define CLOCK_PIN 1
#define DATA_PIN 0
#define PIEZO_PIN A1

int threshold = 500;
int readcycle = 10;

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
}

int getPizeoReading() {
  int sum = 0;
  for(int i=0;i<readcycle;i++) {
    sum += analogRead(PIEZO_PIN);
  }
  return sum / readcycle;
}
void loop()
{
  
        int piezo_read = getPizeoReading();

        int tgtled = map(piezo_read, 0, 1024, 0, NUM_LEDS);
        

          for(int dot = 0; dot < tgtled; dot++) { 
          leds[dot] = CRGB::Blue;
    
          } 
          for(int dot=tgtled;dot<NUM_LEDS;dot++) {
            leds[dot] = CRGB::Red;
          }
          leds[tgtled] = CRGB::Yellow;
                FastLED.show();

}
