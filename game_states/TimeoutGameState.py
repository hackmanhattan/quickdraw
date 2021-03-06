import pygame, sys
from common.Drawable import Image
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
import time
import random

class TimeoutGameState:
	def __init__(self):
		self.background = Image("background_timeout", "assets/images/quickdraw_timeout.jpg", 0,0, True )

	def enter(self):
		# TODO Kill the sound effect from wait here 
		#
    # Wait 30 seconds to switch to home screen
		gv.round_time = 30
		gv.round_start_time = time.time()
		

	def processEvents(self):
		#check if the ready button has been pressed and transit to the title state
		gc.continueCheck(True, "TITLE_SCREEN_STATE")

	def update(self, deltaTime):
    # Increment the timer and exit to the timeout state after 30 seconds
		gv.cur_elapsed = time.time() - gv.round_start_time

		if gv.cur_elapsed > gv.round_time:
      # Timeout to main screen
			changeState("TITLE_SCREEN_STATE")

	def draw(self):
		self.background.draw(gv.screen)
    
	def leave(self):
		pass