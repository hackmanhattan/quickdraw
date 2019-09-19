# import the pygame module, so you can use it
import pygame, sys
from pygame.locals import *
import random
import time
from common import Drawable
from game_states import InitGame, StartRound, ReadyToFire, WinState, Penalty, Timeout
from common.LightController import LightController
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
#mike semko helped
 
# define a main function
def main():
	#begin playing the music
	gv.loadMusic()

	#load the game states into the common array for global access
	gv.gameStates = {
		"TITLE_SCREEN_STATE": InitGame.InitGame(),
		"START_ROUND_STATE": StartRound.StartRound(),
		"READY_TO_FIRE_STATE": ReadyToFire.ReadyToFire(),
		"WIN_STATE": WinState.WinState(),
		"PENALTY_STATE": Penalty.Penalty(),
		"TIMEOUT_STATE": Timeout.Timeout()
  }
	
	# logo = pygame.image.load("logo.jpg")
	# pygame.display.set_icon(logo)
	# pygame.display.set_caption("minimal program")

	#load the lights into a controller for use unless debugging
	if (gv.debug == True):
		import board
		import neopixel
		pixel_pin = board.D18
		# The number of NeoPixels
		num_pixels = 144
		# the number of pixels in a group
		group_size = 24
		pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)
		#Define a new light controller
		gv.lightController = LightController(pixels, group_size)
		gv.lightController.loadPixelsToGroups()



	# define a variable to control the main loop
	running = True
	
	gv.currentState = gv.gameStates["TITLE_SCREEN_STATE"]
	gv.currentState.enter()

	#define deltatime
	accumulated_delta_time = 0

	# main loop
	while running:
			# event handling, gets all event from the eventqueue
			gv.currentState.processEvents()


			#run the updates according to deltatime
			while (accumulated_delta_time > 1/gv.max_framerate):
				gv.currentState.update(1/gv.max_framerate)
				accumulated_delta_time -= (1/gv.max_framerate)
			
			accumulated_delta_time += gv.clock.tick(30) / 1000

			gv.currentState.draw()
			pygame.display.update()
			
			for event in pygame.event.get():
					# only do something if the event is of type QUIT
					if event.type == pygame.QUIT:
							# change the value to False, to exit the main loop
							running = False


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()