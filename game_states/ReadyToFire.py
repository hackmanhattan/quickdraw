import pygame, sys
from common.Drawable import Image
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
import time
import random

class ReadyToFire():
	def __init__(self):
		self.background = Image("background_draw", "quickdraw_draw.jpg", 0,0, True )

	def enter(self):
		# TODO Kill the sound effect from wait here 
		#
    # Give the players 30 seconds to hit the target first
		gv.round_time = 30
		gv.round_start_time = time.time()
		gc.readyToHit()
		

	def processEvents(self):
		if (gc.checkTargets()):
			changeState("WIN_STATE")


	def update(self, deltaTime):
    #Increment the timer and exit to the timeout state after 30 seconds
		gv.cur_elapsed = time.time() - gv.round_start_time

		if gv.cur_elapsed > gv.round_time:
      # TODO Change state to timrout when created
			changeState("TIMEOUT_STATE")

	def draw(self):
		self.background.draw(gv.screen)
    
	def leave(self):
		pass