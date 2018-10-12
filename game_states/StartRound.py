import pygame, sys
from common.Drawable import Image, TextField
from common.GameObject import *
from common.AnimationController import *
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
import time
import random

class StartRound:
	def __init__(self):
		self.background = Image("background_start", "screen_bg.jpg", 0,0, True )
		self.debug = TextField("debug_text", "test", -(gv.screen_width/2) + 100, -(gv.screen_height/2)+40, False)
		self.gameObjects = []
		clintImg = Image("fore_clint", "clint.png", 0,150, True )
		clintObj = GameObject(10,10,True,clintImg)
		self.gameObjects.append(clintObj)
		

	def enter(self):
		#Pause the music and start the round musix
		pauseMusic()
		gv.round_start_effect.play()

		#generate the round interval period
		gv.round_time = random.randint(gv.round_min, gv.round_max)
		gv.round_start_time = time.time()

		#reset clint for his slow travel
		animation = TranslationController(250,0, 600, 0, 10000, True)
		self.gameObjects[0].add_animation(animation)

		#self.foreground.pos_x = 250
		#self.background.pos_x = -50
		#self.background.pos_y = -45
		scale = 1.1
		#self.background.image = pygame.transform.scale(self.background.image, (int(gv.screen_width * scale), int(gv.screen_height * scale)))
		if gv.debug:
			self.debug.drawable = True

	def processEvents(self):
		if (gc.checkHands()):
			changeState("PENALTY_STATE")

	def update(self, deltaTime):
		#Get elapsed time since thr round started
		gv.cur_elapsed = time.time() - gv.round_start_time

		#traverse the parallax
		#self.foreground.pos_x += (.125 * deltaTime)
		self.background.pos_x -= (.0125 * deltaTime)

		#display a counter for debug purposes
		if gv.debug:
			self.debug.text = str(round(gv.cur_elapsed, 3))

		#Check to see if the round is over
		if gv.cur_elapsed > gv.round_time:
			changeState("READY_TO_FIRE_STATE")

		for obj in self.gameObjects:
			obj.update(deltaTime)

	def draw(self):
		self.background.draw(gv.screen)
		#self.foreground.draw(gv.screen)
		self.debug.draw(gv.screen)
		for obj in self.gameObjects:
			obj.draw(gv.screen)
    
	def leave(self):
		pass