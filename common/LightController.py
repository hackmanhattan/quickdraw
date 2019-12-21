import time

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
  _currentAnimation = "None"

  def __init__(self, led_range, group_size, pixels):
    print('initializing light group starting with' + str(led_range) + ' with group size ' + str(group_size))
    self._pixels = pixels
    self._group_size = group_size
    self._leds = led_range
    self.time = time

  #control functions for the lights themselves
  def globalChangeAll(self, r,g,b, i=1, show=True):
    self._color_1 = Color(r,g,b)
    self._pixels.fill(self._color_1.intensity(i))
    if show:  
      self._pixels.show()


  def changeAll(self, r, g, b, i=1, show=True):
    print('changing all lights to ' + str(r) + ', ' + str(g) + ', ' + str(b) + ' at level ' + str(i))
    self._color_1 = Color(r,g,b)
    self._pixels.fill_range(self._color_1.intensity(i),self._leds, self._leds + self._group_size)
    # for l in range(self._leds, self._leds + self._group_size):
    #   self._pixels[l] = self._color_1.intensity(i)
    if show:  
      self._pixels.show()

  def changeOdd(self, r, g, b, i=1, show=True):
    self._color_1 = Color(r,g,b)
    print('changing odd lights to ' + str(r) + ', ' + str(g) + ', ' + str(b) + ' at level ' + str(i))
    for l in range(self._leds + 1, self._leds + self._group_size, 2):
      self._pixels[l] = self._color_1.intensity(i)
    if show:  
      self._pixels.show()

  def changeEven(self, r, g, b, i=1, show=True):
    self._color_2 = Color(r,g,b)
    print('changing even lights to ' + str(r) + ', ' + str(g) + ', ' + str(b) + ' at level ' + str(i))
    for l in range(self._leds, self._leds + self._group_size, 2):
      self._pixels[l] = self._color_2.intensity(i)
    if show:  
      self._pixels.show()

  def changeOne(self, led, r, g, b, i=1):
    print('changing led ' + str(led) + ' to ' + str(r) + ', ' + str(g) + ', ' + str(b) + ' at level ' + str(i))
    self._pixels[led] = (int(r/i),int(g/i),int(b/i))

  def changeInPercSeq(self, color, percentLit, lightGroupStart, lightGroupEnd, i=1):
    print('lighting lights from start to finish')
    led_range_size = (lightGroupEnd._leds + self._group_size) - lightGroupStart._leds
    fillRangeEnd = (led_range_size * percentLit) + lightGroupStart._leds

    self._pixels.fill_range(color.intensity(i), self._leds, fillRangeEnd)
    # for l in range(lightGroupStart._leds, lightGroupEnd + self._group_size):
    self._pixels.show()

  
  
  #Different Light animations
  def fadeIn(self, color):
    timeTilTarget = self.timeRemaining()
    total_time = self.totalTime()
    self.changeAll( color.r,color.g,color.b, 1 - (timeTilTarget / total_time) )
  def fadeOut(self, color):
    timeTilTarget = self.timeRemaining()
    total_time = self.totalTime()
    self.changeAll( color.r,color.g,color.b, 0 + (timeTilTarget / total_time) )
  def globalFadeIn(self, color):
    timeTilTarget = self.timeRemaining()
    total_time = self.totalTime()
    self.globalChangeAll( color.r,color.g,color.b, 1 - (timeTilTarget / total_time) )
  def globalFadeOut(self, color):
    timeTilTarget = self.timeRemaining()
    total_time = self.totalTime()
    self.globalChangeAll( color.r,color.g,color.b, 0 + (timeTilTarget / total_time) )
  def alternate(self):
    if self._currentAnimation == 'Alt1':
      self.changeEven(self._color_1.r, self._color_1.g, self._color_1.b)
      self.changeOdd(self._color_2.r, self._color_2.g, self._color_2.b)
    else:
      self.changeEven(self._color_2.r, self._color_2.g, self._color_2.b)
      self.changeOdd(self._color_1.r, self._color_1.g, self._color_1.b)
    if self.timeRemaining() <= 50:
      if self._currentAnimation == 'Alt1':
        self.setAlternate(self.totalTime(), 'Alt2')
      else:
        self.setAlternate(self.totalTime())

  
  #TIME math
  #Get time remaining on current animation
  def timeRemaining(self):
    return self.target_time - self.curr_time
  #Get the total time the animation was set for
  def totalTime(self):
    return self.target_time - self.start_time

    

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
  def clearAnim(self):
    self.active = False
    self._currentAnimation = 'None'

  def setGlow(self, new_time, color, dir):
    self.setupBasicPattern(new_time, color, dir)

  def setFlash(self, fadeTime, color):
    #light up target immediately and fade away
    self.changeAll(color.r, color.g, color.b)
    self.setupBasicPattern(fadeTime, color, "Flash")

  def setSpiral(self):
    pass
  
  def setAlternate(self, alt_time, dir='Alt1'):
    self.setupTime(alt_time)
    self.active = True
    self._currentAnimation = dir

  def setupBasicPattern(self, new_time, color, animation):
    self.active = True
    self._color_1 = color
    self._currentAnimation = animation
    self.setupTime(new_time)
  
  def setupTime(self, new_time):
    self.target_time = self.time.time() + new_time / 1000
    self.start_time = self.time.time()
    self.curr_time = self.time.time()

  #relevant commands for the game loop
  def tick(self, deltaTime):
    if (self.curr_time >= self.target_time):
      if (self._currentAnimation != 'GlowFadeIn' and self._currentAnimation != 'GlowFadeOut'):
        self.active = False
        self._currentAnimation = 'None'
      else:
        if (self._currentAnimation == 'GlowFadeIn'):
          self.setGlow(500, self._color_1, 'GlowFadeOut')
        else:
          self.setGlow(500, self._color_1, 'GlowFadeIn')

    self.curr_time += deltaTime

  def animate(self):
    if (self._currentAnimation == 'GlowFadeIn'):
      self.globalFadeIn(self._color_1)
    elif (self._currentAnimation == 'GlowFadeOut'):
      self.globalFadeOut(self._color_1)
    elif (self._currentAnimation == 'Flash'):
      self.fadeOut(self._color_1)
    elif (self._currentAnimation == 'Alt1' or self._currentAnimation == 'Alt2'):
      self.alternate()
    
# import board
# import neopixel
  
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

