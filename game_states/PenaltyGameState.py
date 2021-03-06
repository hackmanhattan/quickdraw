import pygame, sys
from common.Drawable import Image, TextField
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
import time
import random

class PenaltyGameState:
	def __init__(self):
		self.background = Image("background_penalty", "assets/images/quickdraw_penalty.jpg", 0,0, True )
		self.text = TextField("penalty", "test", 350, -60, True, color=(255,255,255))

	def enter(self):
		# TODO Kill the sound effect from wait here 
		#
    # Wait 30 seconds to switch to home screen
		gv.round_time = 30
		gv.round_start_time = time.time()

		#Reveal the play who initiated a penalty
		self.text.text = "Player " + str(gv.penalty)
		

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
		self.text.draw(gv.screen)
    
	def leave(self):
		#TODO do it right
		time.sleep(2)
		pass
