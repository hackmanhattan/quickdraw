# import the pygame module, so you can use it
import pygame, sys
from pygame.locals import *
import random
import time
from common import Drawable
from game_states import TitleScreenGameState, StartRoundGameState, ReadyToFireGameState, WinGameState, PenaltyGameState, TimeoutGameState, InitGameState
from common.LightController import LightController
from common.Common import globalVars as gv
from common.Common import *
from common.Inputs import gameController as gc
from common.GameObject import *
#mike semko helped
 
# define a main function
def main():
	#begin playing the music
	gv.loadMusic()

	#load the game states into the common array for global access
	gv.gameStates = {
		"INIT_GAME_STATE": InitGameState.InitGameState(),
		"TITLE_SCREEN_STATE": TitleScreenGameState.TitleScreenGameState(),
		"START_ROUND_STATE": StartRoundGameState.StartRoundGameState(),
		"READY_TO_FIRE_STATE": ReadyToFireGameState.ReadyToFireGameState(),
		"WIN_STATE": WinGameState.WinGameState(),
		"PENALTY_STATE": PenaltyGameState.PenaltyGameState(),
		"TIMEOUT_STATE": TimeoutGameState.TimeoutGameState()
  }
	
	# logo = pygame.image.load("logo.jpg")
	# pygame.display.set_icon(logo)
	# pygame.display.set_caption("minimal program")

	#load the lights into a controller for use unless debugging
	if (gv.debug == False):
		import board
		from libs.neopixel_mod import NeoPixel as neopixel
		pixel_pin = board.D21
		# The number of NeoPixels
		num_pixels = 144
		# the number of pixels in a group
		group_size = 24
		pixels = neopixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)
		#Define a new light controller
		gv.lightController = LightController(pixels, group_size)
		gv.lightController.loadPixelsToGroups()

	#setup the lights as a global for all states to access
	if (gv.debug == False):
		gv.lightsObject = GameObject(0,0,False)
		for light in gv.lightController.getLights():
			gv.lightsObject.add_light(light)



	# define a variable to control the main loop
	running = True
	
	gv.currentState = gv.gameStates["INIT_GAME_STATE"]
	gv.currentState.enter()

	#define deltatime
	accumulated_delta_time = 0

	# main loop
	while running:
		
		if len(pygame.event.get(pygame.QUIT)) >= 1:
			running = False

		# events = pygame.event.get()
		# for event in events:
		# 	print(len(events))
		# 	print(event.type)
		# 	if (event.type == pygame.KEYUP):
		# 		if event.key == pygame.K_ESCAPE:
		# 			running = False
		# 		else:
		# 			pygame.event.post(event)
		# 			pass

		# event handling, gets all event from the eventqueue
		gv.currentState.processEvents()
		
		
		#run the updates according to deltatime
		while (accumulated_delta_time > 1/gv.max_framerate):
			gv.currentState.update(1/gv.max_framerate)
			accumulated_delta_time -= (1/gv.max_framerate)

		accumulated_delta_time += gv.clock.tick(30) / 1000

		gv.currentState.draw()
		pygame.display.update()


		# for event in pygame.event.get():
		# 		# only do something if the event is of type QUIT
		# 		print(event)
		# 		if event.type == pygame.QUIT:
		# 				# change the value to False, to exit the main loop
		# 				running = False


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()