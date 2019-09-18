import time
import board
import neopixel

class lightController():
  _pixels = None
  _group_size = None
  _lights = []
  def __init__(self, pixels, group_size):
    self._pixels = pixels
    self._group_size = group_size
    
  def loadPixelsToGroups(self):
    for i in range( 0, self._pixels.numPixels, self._group_size ):
      self._lights.append(lightGroup( i, self._group_size, self._pixels))
      pass

    pixels.show()

  def getLights(self):
    return self._lights

  

class lightGroup():
  _leds = []
  _pixels = None
  _group_size = 0
  def __init__(self, led_range, group_size, pixels):
    self._pixels = pixels
    self._group_size = group_size
    for l in range(led_range, led_range + group_size):
      self._leds.append(led_range[l])

  def changeAll(self, r, g, b, i, time):
    self._pixels.fill(pixels.Color(r,g,b), self._leds[0], self._group_size )
    self._pixels.show()

  def changeOdd(self, r, g, b, i, time):
    for i in range(1, len(self._leds), 2):
      self._pixels[self._pixels + i].setPixelColor(r,g,b)
      self._pixels.show()

  def changeEven(self, r, g, b, i, time):
    for i in range(0, len(self._leds), 2):
      self._pixels[self._pixels + i].setPixelColor(r,g,b)
      self._pixels.show()
  
#neopixel setup

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
 
# The number of NeoPixels
num_pixels = 30
# the number of pixels in a group
group_size = 17
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
 
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.0, auto_write=False,
                           pixel_order=ORDER)

#Define a new light controller
target_led_controller = lightController(pixels, group_size)

lights = target_led_controller.getLights()

#turn the light groups on one at a time
for i in range(0, len(lights)):
  lights[i].changeAll(255, 0, 0, 100, 60)
  time.sleep(1)
