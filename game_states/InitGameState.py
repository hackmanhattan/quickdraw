import pygame, sys
from common.Drawable import Image, TextField, Fill
from common.GameObject import *
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
from common.AnimationController import *
import time
import random

class InitGame:
  def __init__(self):
    pass
    # self.background = Image("background_timeout", "quickdraw_timeout.jpg", 0,0, True )
    self.background = Fill('white_bg', (255,255,255))
    self.gameObjects = []
    gameImage = Image("logo", "assets/images/lol.jpg", gv.screen_width/2-256,gv.screen_height/2-172, False )
    logo = GameObject(gv.screen_width/2-256,gv.screen_height/2-172,True,gameImage)
    hm_gameImage = Image("logo", "assets/images/hm_logo.png", gv.screen_width/2-256,gv.screen_height/2-172, False )
    hm_logo = GameObject(gv.screen_width/2-133,gv.screen_height/2-154,True,hm_gameImage)
    
    logo.add_animation(OpacityController(0,1,2, True))
    self.gameObjects.append(logo)
    self.gameObjects.append(hm_logo)
    self.hideLogo = False
    self.showHm = False

  def enter(self):
    self.logo_fader = 5
    self.load_title = 8
    gv.round_start_time = time.time()
    # pygame.time.set_timer(USEREVENT+1, 100)

    

  def processEvents(self):

    # event = pygame.event.poll()
    # while event.type != pygame.NOEVENT:
    #   if event.type == pygame.KEYUP:
    #     print("key up triggered")
    #   elif event.type == USEREVENT+1:
    #     print('beep')
    #     self.gameObjects[0].add_animation(OpacityController(1,0,2, True))

    # events = pygame.event.get()
    # for event in events:
    #   print(len(events))
    #   print(event.type)
    #   if event.type == pygame.KEYUP:
    #     print("key up triggered")
      # elif event.type == USEREVENT+1:
      #   print('beep')
      #   self.gameObjects[0].add_animation(OpacityController(1,0,2, True))

    gv.cur_elapsed = time.time() - gv.round_start_time
    # if gv.cur_elapsed > self.logo_fader:
    if (self.hideLogo == False) and (self.gameObjects[0].animations[0].active == False):
      self.gameObjects[0].add_animation(OpacityController(1,0,2, True))
      self.hideLogo = True
    if (self.hideLogo == True) and (self.showHm == False) and (self.gameObjects[0].animations[1].active == False):
      self.gameObjects[1].add_animation(OpacityController(0,1,2, True))
      self.showHm = True

    if gv.cur_elapsed > self.load_title:
      changeState("TITLE_SCREEN_STATE")
    pass

  def update(self, deltaTime):
    for obj in self.gameObjects:
    	obj.update(deltaTime)
    pass

  def draw(self):
    self.background.draw(gv.screen)
    for obj in self.gameObjects:
      obj.draw(gv.screen)
    pass
    
  def leave(self):
    pass