import pygame, sys
from common.Drawable import Image
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
import time
import random

class StartRound:
	def __init__(self):
		self.foreground = Image("fore_clint", "clint.png", 0,150, True )
		self.background = Image("background_start", "screen_bg.jpg", 0,0, True )

	def enter(self):
		global round_time
		global round_start_time
		pauseMusic()
		gv.round_start_effect.play()
		gv.round_time = random.randint(gv.round_min, gv.round_max)
		gv.round_start_time = time.time()
		#reset clint for his slow travel
		self.foreground.pos_x = 250
		self.background.pos_x = -50
		self.background.pos_y = -45
		scale = 1.1
		self.background.image = pygame.transform.scale(self.background.image, (int(gv.screen_width * scale), int(gv.screen_height * scale)))

	def processEvents(self):
		if (gc.checkHands()):
			changeState("PENALTY_STATE")

	def update(self):
		global cur_elapsed
		gv.cur_elapsed = time.time() - gv.round_start_time
		self.foreground.pos_x += .5
		self.background.pos_x -= .25
		if gv.cur_elapsed > gv.round_time:
			changeState("READY_TO_FIRE_STATE")

	def draw(self):
		self.background.draw(gv.screen)
		self.foreground.draw(gv.screen)
    
	def leave(self):
		pass