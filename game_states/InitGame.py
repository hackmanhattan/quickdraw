import pygame, sys
from common.Drawable import Image
from common.Common import *
from common.Common import globalVars as gv
from common.Inputs import gameController as gc

class InitGame:
  def __init__(self):
    self.background = Image("background_title", "quickdraw_title_b.jpg", 0,0, True )

  def enter(self):
    #Turn the music on if not playing, checks at beginning of init to make sure, unpauses when re-entering state
    if not gv.musicIsOn:
      gv.musicIsOn = True
      gv.music.play()
    #if any sounds are playing, stop them
    pygame.mixer.stop()

    unpauseMusic()
    #self.background.animate(200, 200, 2000)

  def processEvents(self):
    #check if the ready button has been pressed and transit to the start state
    gc.checkReady(True, "START_ROUND_STATE")

  def update(self, deltaTime):
    pass

  def draw(self):
    self.background.draw(gv.screen)

  def leave(self):
    pass