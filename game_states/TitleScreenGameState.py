import pygame, sys
from common.Drawable import Image
from common.GameObject import *
from common.AnimationController import *
from common.Common import *
from common.Common import globalVars as gv
from common.Inputs import gameController as gc
from common.LightController import Color

class TitleScreenGameState:
  def __init__(self):
    self.background = Image("background_title", "assets/images/quickdraw_title.jpg", 0,0, True )
    self.gameObjects = []
    gameImage = Image("crosshairs", "assets/images/crosshair.png", 0,0, True, alpha=True )
    gameObject = GameObject(10,10,True,gameImage)
    self.gameObjects.append(gameObject)
    self.text = TextField("readyTxt", "test", 200, 400, True)
    self.text2 = TextField("readyTxt", "test", 200, 300, True)

  def addGameObj(self, gameObject):
    self.gameObjects.append(gameObject)
  
  def removeGameObj(self, target):
    self.gameObjects.remove(target)

  def enter(self):
    #Turn the music on if not playing, checks at beginning of init to make sure, unpauses when re-entering state
    if not gv.musicIsOn:
      gv.musicIsOn = True
      gv.music.play()
    #if any sounds are playing, stop them
    pygame.mixer.stop()
    unpauseMusic()
    animation = TranslationController(10,10, 1400, 700, 10000, True)
    rotation = RotationController(0, 360, 5000, True)
    self.gameObjects[0].add_animation(animation)
    self.gameObjects[0].add_animation(rotation)
    self.addGameObj(gv.lightsObject)
    # for light in gv.lightsObject.lights:
    #   light.setGlow(500, Color(255,0,0), 'GlowFadeIn')
    # gv.lightsObject.lights[0].setGlow(500, Color(255,0,0), 'GlowFadeIn')


  def processEvents(self):
    #check if the ready button has been pressed and transit to the start state
    gc.checkReady(True, "SINGLE_PLAYER_STATE", "MULTIPLAYER_STATE")

  def update(self, deltaTime):
    self.text.text = "Multiplayer Ready: " + str(round(gv.multiPlayerReadyCount,3)) + " seconds"
    self.text2.text = "Single player Ready: " + str(round(gv.singlePlayerReadyCount,3)) + " seconds"
    for obj in self.gameObjects:
      obj.update(deltaTime)

  def draw(self):
    self.background.draw(gv.screen)
    self.text.draw(gv.screen)
    self.text2.draw(gv.screen)
    for obj in self.gameObjects:
      obj.draw(gv.screen)

  def leave(self):
    #cleanup after yourself
    for light in gv.lightsObject.lights:
      light.clearAnim()
    self.removeGameObj(gv.lightsObject)
    pass