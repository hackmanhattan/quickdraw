import time
import board
import neopixel

class LightController():
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
      self._lights.append(LightGroup( i, self._group_size, self._pixels))
      pass
    print('All groups loaded')
    pixels.show()

  def getLights(self):
    return self._lights

class LightGroup():
  _leds = 0
  _pixels = None
  _group_size = 0
  target_time = 0
  curr_time = 0
  start_time = 0
  _r = 0
  _g = 0
  _b = 0
  active = False
  _currentAnimation = "Glow"

  def __init__(self, led_range, group_size, pixels):
    print('initializing light group starting with' + led_range + ' with group size ' + group_size)
    self._pixels = pixels
    self._group_size = group_size
    self._leds = led_range
    self.time = time
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
  
  def fadeIn(self, r,g,b):
    self.changeAll( r,g,b, self.curr_time / self.target_time )
  def fadeOut(self, r,g,b):
    self.changeAll( r,g,b, 1 - (self.curr_time / self.target_time) )

  def setGlow(self, new_time, r, g, b, dir):
    self.target_time = self.time + new_time
    self.start_time = self.time
    self.curr_time = self.time
    self.active = True
    self._r = r
    self._g = g
    self._b = b
    self._currentAnimation = dir

  def tick(self, deltaTime):
    if (self.time >= self.target_time):
      if (self._currentAnimation != 'GlowFadeIn' or self._currentAnimation != 'GlowFadeOut'):
        self.active = False
      else:
        if (self._currentAnimation == 'GlowFadeIn'):
          self.setGlow(1000, self._r, self._g, self._b, 'GlowFadeOut')
        else:
          self.setGlow(1000, self._r, self._g, self._b, 'GlowFadeIn')

    self.curr_time += deltaTime

  def animate(self, targetObj):
    if (self._currentAnimation == 'GlowFadeIn'):
      self.fadeIn(self._r, self._g, self._b)
    elif (self._currentAnimation == 'GlowFadeOut'):
      self.fadeOut(self._r, self._g, self._b)
    

    
  
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
target_led_controller = LightController(pixels, group_size)

lights = target_led_controller.getLights()

#turn the light groups on one at a time
for i in range(0, len(lights)):
  lights[i].changeAll(255, 0, 0, 100, 60)
  time.sleep(1)
