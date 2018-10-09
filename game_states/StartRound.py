import pygame, sys
from lib.Drawable import Image
from lib.Common import globalVars as gv
from lib.Common import *
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

	def processEvents(self):
		pass

	def update(self):
		global cur_elapsed
		gv.cur_elapsed = time.time() - gv.round_start_time
		self.foreground.pos_x += 1
		if gv.cur_elapsed > gv.round_time:
			changeState("READY_TO_FIRE_STATE")

	def draw(self):
		self.background.draw(gv.screen)
		self.foreground.draw(gv.screen)
    
	def leave(self):
		pass