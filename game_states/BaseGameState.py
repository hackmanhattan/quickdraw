import pygame, sys
from common.Drawable import Image, TextField
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
import time
import random

class BaseGameState:
  def __init__(self):
    pass
    #self.background = Image("assets/images/background_timeout", "quickdraw_timeout.jpg", 0,0, True )
    #
    # self.gameObjects = []
    # clintImg = Image("fore_clint", "assets/images/clint.png", 0,250, True )
    # clintObj = GameObject(10,10,True,clintImg)
    # self.gameObjects.append(clintObj)
    #
    # self.text = TextField("Example_text", "Initial text, never seen", 0, 0, True, color=(255,255,255))
    # 

  def enter(self):
    # self.text.text = "Text for the player to see"
    pass
    

  def processEvents(self):
    pass

  def update(self, deltaTime):
    # for obj in self.gameObjects:
    # 	obj.update(deltaTime)
    pass

  def draw(self):
    #self.background.draw(gv.screen)
    pass
    
  def leave(self):
    pass