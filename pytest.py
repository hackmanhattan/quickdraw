# import the pygame module, so you can use it
import pygame, sys
from pygame.locals import *
import random
import time
from lib import Drawable
from game_states import InitGame, StartRound, ReadyToFire, WinState, Penalty, Timeout
from lib.Common import globalVars as gv
from lib.Common import *
from lib.Inputs import gameController as gc
 
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

	# define a variable to control the main loop
	running = True
	
	gv.currentState = gv.gameStates["TITLE_SCREEN_STATE"]
	gv.currentState.enter()

	# main loop
	while running:
			gv.clock.tick(30)
			# event handling, gets all event from the eventqueue
			gv.currentState.processEvents()
			gv.currentState.update()
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