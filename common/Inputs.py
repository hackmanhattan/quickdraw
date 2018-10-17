import pygame, time
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
				#delay detection so that it does not progress too quickly
				time.sleep(0.25)
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
	
	#Check to see if any of the targets have been hit
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
	
	#Check if the players hands are on the button and return true if they remove it early
	def checkHands():
		if (gv.debug):
			keys=pygame.key.get_pressed()
			if (keys[pygame.K_a]):
				gv.penalty = 1
				return True
			if (keys[pygame.K_s]):
				gv.penalty = 2
				return True
		else:
			#setup button press monitoring here
			pass

	













