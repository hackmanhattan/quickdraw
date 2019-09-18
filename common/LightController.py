import time
import board
import neopixel

class lightController():
  _pixels = None
  _group_size = 0
  _lights = []
  def __init__(self, pixels, group_size):
    print('initializing light controller')
    self._pixels = pixels
    self._group_size = group_size
    
  def loadPixelsToGroups(self):
    print('loading pixels to group...')
    for i in range( 0, len(self._pixels), self._group_size ):
      print('loading group ' + i)
      self._lights.append(lightGroup( i, self._group_size, self._pixels))
      pass
    print('All groups loaded')
    pixels.show()

  def getLights(self):
    return self._lights

class lightGroup():
  _leds = 0
  _pixels = None
  _group_size = 0
  def __init__(self, led_range, group_size, pixels):
    print('initializing light group starting with' + led_range + ' with group size ' + group_size)
    self._pixels = pixels
    self._group_size = group_size
    self._leds = led_range
  def changeAll(self, r, g, b, i=1):
    print('changing all lights to ' + r + ', ' + g + ', ' + b + ' at level ' + i)
    for l in range(self._leds, self._leds + self._group_size):
      self._pixels[self._leds + l] = (r/i,g/i,b/i)
      self._pixels.show()
  def changeOdd(self, r, g, b, i=1):
    print('changing odd lights to ' + r + ', ' + g + ', ' + b + ' at level ' + i)
    for l in range(self._leds + 1, self._leds + self._group_size, 2):
      self._pixels[self._pixels + l] = (r/i,g/i,b/i)
      self._pixels.show()
  def changeEven(self, r, g, b, i=1):
    print('changing even lights to ' + r + ', ' + g + ', ' + b + ' at level ' + i)
    for l in range(self._leds, self._leds + self._group_size, 2):
      self._pixels[self._pixels + l] = (r/i,g/i,b/i)
      self._pixels.show()
  def changeOne(self, led, r, g, b, i=1):
    print('changing led ' + led + ' to ' + r + ', ' + g + ', ' + b + ' at level ' + i)
    self._pixels[led] = (r/i,g/i,b/i)
  
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
