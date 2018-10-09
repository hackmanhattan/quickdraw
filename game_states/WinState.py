import pygame, sys
from common.Drawable import Image, TextField
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
import time
import random

class WinState:
	def __init__(self):
		self.bg1 = Image("background_p1win", "quickdraw_p1win.jpg", 0,0, True )
		self.bg2 = Image("background_p2win", "quickdraw_p2win.jpg", 0,0, True )
		self.background = self.bg1
		self.text = TextField("win_text", "test", 200, 400, True)

	def enter(self):
		# TODO Kill the sound effect from wait here 
		#
    # Wait 30 seconds to switch to home screen
		if (gv.winner == 1):
			self.background = self.bg1
		else:
			self.background = self.bg2
		gv.round_time = 30
		gv.round_start_time = time.time()

		#Reveal the time for the player who won to hit the target
		lastTime = gv.cur_elapsed
		self.text.text = "Time elapsed " + str(lastTime) + " seconds"
		

	def processEvents(self):
		#check if the ready button has been pressed and transit to the title state
		gc.checkReady(True, "TITLE_SCREEN_STATE")

	def update(self):
    # Increment the timer and exit to the timeout state after 30 seconds
		gv.cur_elapsed = time.time() - gv.round_start_time

		if gv.cur_elapsed > gv.round_time:
      # Timeout to main screen
			changeState("TITLE_SCREEN_STATE")

	def draw(self):
		self.background.draw(gv.screen)
		self.text.draw(gv.screen)
    
	def leave(self):
		pass