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
      print('loading group ' + str(i))
      self._lights.append(LightGroup( i, self._group_size, self._pixels))
      pass
    print('All groups loaded')
    self._pixels.show()

  def getLights(self):
    return self._lights

#functional class to hold color data neatly
class Color():
  _rgb = (0,0,0)
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b
    self._rgb = (r,g,b)
  def intensity(self, intensity):
    return ( int(self.r*intensity), int(self.g*intensity), int(self.b*intensity) )
  def white(self):
    return (255,255,255)

class LightGroup():
  _leds = 0
  _pixels = None
  _group_size = 0
  target_time = 0
  curr_time = 0
  start_time = 0
  _color_1 = Color(0,0,0)
  _color_2 = Color(0,0,0)
  _color_3 = Color(0,0,0)
  _color_4 = Color(0,0,0)
  active = False
  _currentAnimation = "GlowFadeIn"

  def __init__(self, led_range, group_size, pixels):
    print('initializing light group starting with' + str(led_range) + ' with group size ' + str(group_size))
    self._pixels = pixels
    self._group_size = group_size
    self._leds = led_range
    self.time = time

  #control functions for the lights themselves
  def changeAll(self, r, g, b, i=1):
    print('changing all lights to ' + str(r) + ', ' + str(g) + ', ' + str(b) + ' at level ' + str(i))
    self._color_1 = Color(r,g,b)
    for l in range(self._leds, self._leds + self._group_size - 1):
      self._pixels[l] = self._color_1.intensity(i)
      self._pixels.show()

  def changeOdd(self, r, g, b, i=1):
    self._color_1 = Color(r,g,b)
    print('changing odd lights to ' + str(r) + ', ' + str(g) + ', ' + str(b) + ' at level ' + str(i))
    for l in range(self._leds + 1, self._leds + self._group_size - 1, 2):
      self._pixels[l] = self._color_1.intensity(i)
      self._pixels.show()

  def changeEven(self, r, g, b, i=1):
    self._color_2 = Color(r,g,b)
    print('changing even lights to ' + str(r) + ', ' + str(g) + ', ' + str(b) + ' at level ' + str(i))
    for l in range(self._leds, self._leds + self._group_size - 1, 2):
      self._pixels[l] = self._color_2.intensity(i)
      self._pixels.show()

  def changeOne(self, led, r, g, b, i=1):
    print('changing led ' + str(led) + ' to ' + str(r) + ', ' + str(g) + ', ' + str(b) + ' at level ' + str(i))
    self._pixels[led] = (int(r/i),int(g/i),int(b/i))
  
  #Different Light animations
  def fadeIn(self, color):
    timeTilTarget = self.target_time - self.curr_time
    total_time = self.target_time - self.start_time
    self.changeAll( color.r,color.g,color.b, 1 - (timeTilTarget / total_time) )
  def fadeOut(self, color):
    timeTilTarget = self.target_time - self.curr_time
    total_time = self.target_time - self.start_time
    self.changeAll( color.r,color.g,color.b, 0 + (timeTilTarget / total_time) )

  #Have up to 4 colors saved
  def setColor1(self, r,g,b):
    self._color_1 = (r,g,b)
  def setColor2(self, r,g,b):
    self._color_2 = (r,g,b)
  def setColor3(self, r,g,b):
    self._color_3 = (r,g,b)
  def setColor4(self, r,g,b):
    self._color_4 = (r,g,b)

  #setup animation patterns here
  def setGlow(self, new_time, color, dir):
    self.setupBasicPattern(new_time, color, dir)

  def setFlash(self, fadeTime, color):
    #light up target immediately and fade away
    self.changeAll(color.r, color.g, color.b)
    self.setupBasicPattern(fadeTime, color, "Flash")

  def setSpiral(self):
    pass
  
  def setAlternate(self):
    pass

  def setupBasicPattern(self, new_time, color, animation):
    self.active = True
    self.target_time = self.time.time() + new_time
    self.start_time = self.time.time()
    self.curr_time = self.time.time()
    self._color_1 = color
    self._currentAnimation = animation

  #relevant commands for the game loop
  def tick(self, deltaTime):
    if (self.curr_time >= self.target_time):
      if (self._currentAnimation != 'GlowFadeIn' and self._currentAnimation != 'GlowFadeOut'):
        self.active = False
        self._currentAnimation = 'None'
      else:
        if (self._currentAnimation == 'GlowFadeIn'):
          self.setGlow(1000, self._color_1, 'GlowFadeOut')
        else:
          self.setGlow(1000, self._color_1, 'GlowFadeIn')

    self.curr_time += deltaTime

  def animate(self):
    if (self._currentAnimation == 'GlowFadeIn'):
      self.fadeIn(self._color_1)
    elif (self._currentAnimation == 'GlowFadeOut'):
      self.fadeOut(self._color_1)
    elif (self._currentAnimation == 'Flash'):
      self.fadeOut(self._color_1)
    

    
  
# #neopixel setup

# # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# # NeoPixels must be connected to D10, D12, D18 or D21 to work.
# pixel_pin = board.D21
 
# # The number of NeoPixels
# num_pixels = 144
# # the number of pixels in a group
# group_size = 24
 
# pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.0, auto_write=False)

# #Define a new light controller
# target_led_controller = LightController(pixels, group_size)
# target_led_controller.loadPixelsToGroups()
# lights = target_led_controller.getLights()

