import pygame
from common.Common import *
from common.Common import globalVars as gv

if (gv.debug == False):
	import Adafruit_GPIO.SPI as SPI
	import Adafruit_MCP3008

class gameController():
	def __init__(self):
		pass

	if (gv.debug):
		playerOneReady = True
		playerTwoReady = True
		targetOne = pygame.K_1
		targetTwo = pygame.K_2
		targetThree = pygame.K_3
		targetFour = pygame.K_4
		targetFive = pygame.K_5
		targetSix = pygame.K_6
		readyBtn = pygame.K_SPACE
	else:
		#Setup the analog reader here
		mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))
		pass

	def checkReady(self, state):
		if (gv.debug):
			#Get the currently pressed keys
			keys=pygame.key.get_pressed()
			if keys[gameController.readyBtn]:
				changeState(state)
		else:
			#setup the analog button here
			pass

	def pollAdc(self):
		#poll the MCP3008 for the actual target readouts
		values = [0]*8
		for j in range(0, signal_reads):
			for i in range(8):
				values[i] +=  mcp.read_adc(i)
			for i in range(0,8):
				values[i] = values[i] / (signal_reads *1.0)
			return values
	
	def checkTargets():
		if (gv.debug):
			#Get the currently pressed keys
			keys=pygame.key.get_pressed()
			if ( 
				keys[gameController.targetOne] | 
				keys[gameController.targetTwo] |
				keys[gameController.targetThree]
				):
				gv.winner = 1
				return True
			elif (
				keys[gameController.targetFour] |
				keys[gameController.targetFive] |
				keys[gameController.targetSix] 
				):
				gv.winner = 2
				return True
			else:
				return False
		else:
			#setup the system to return true or false based on analog reader
			pass

	













