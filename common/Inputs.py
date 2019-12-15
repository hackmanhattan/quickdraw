import pygame, time
from common.Common import *
from common.Common import globalVars as gv

if (gv.debug == False):
	import Adafruit_GPIO.SPI as SPI
	import Adafruit_MCP3008

impactThreshold = 30
targetCount = 6
class gameController():
	target_state = [0]*targetCount #0=round start, 1 = target ready, 2 =target hit
	prevBtnState = []
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
	else:
		#Setup the analog reader here
		CLK = 18
		MISO = 23
		MOSI = 24
		CS = 25
		mcp = Adafruit_MCP3008.MCP3008(clk=CLK,cs=CS,miso=MISO,mosi=MOSI)
		print("mcp initalized")
		pass
	readyBtn = pygame.K_SPACE
	quitBtn = pygame.K_ESCAPE
	def checkReady(self, state):
		#Get the currently pressed keys
		keys=pygame.key.get_pressed()
		values = gameController.pollAdc()
		#TODO do not start game immediately. show animation like Death Stranding UI for selection structure option
		curBtnState = gameController.getBtnState(values)
		deltaBtnState = curBtnState ==  gameController.prevBtnState
		# if prevBtnState is not the same as current
		if keys[gameController.readyBtn]:
			changeState(state)
			#delay detection so that it does not progress too quickly
			time.sleep(0.25)
		elif curBtnState == [True, True]:
			changeState(state)
			time.sleep(0.25)
		elif keys[gameController.quitBtn]:
			pygame.quit()
		elif keys[pygame.K_RALT] and keys[pygame.K_RETURN]:
			pygame.display.toggle_fullscreen()
		gameController.prevBtnState = curBtnState
	def getBtnState(values):
		retlist = []
		for i in range(6,8):
			if values[i]<1020.0 and values[i]>10.0:
				retlist.append(False)
			else:
				retlist.append(True)
		return retlist
	def readyToHit():
		#1 = target ready
		for i in range(0,targetCount):
			gameController.target_state[i] = 1 
			# change target color to hit me mode
			for light in gv.lightController.getLights():
				light.changeAll(0,255,0,1,False)
			gv.lightController._pixels.show()
	def pollAdc():
		#poll the MCP3008 for the actual target readouts
		# signal_reads is # of read cycles to average output
		# sums read values from each channnel on 8pins
		# return is an average read value for each channel
		signal_reads = 1
		values = [0]*8
		for j in range(0, signal_reads):
			for i in range(8):
				values[i] +=  gameController.mcp.read_adc(i)
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
				# logic for reading signals and toggling target changes
				values = gameController.pollAdc()
				for i in range(0,targetCount):
					if values[i]>impactThreshold and target_state[i] is 1:
						target_state[i] = 2
						# TODO: code to change target color
						# TODO: check if winner
						if sum(target_state[0:3]) is 6:
							gv.winner = 1
						elif sum(target_state[3:6]) is 6:
							gv.winner = 2
				return False
		else:
			#setup the system to return true or false based on analog reader
			# logic for reading signals and toggling target changes
			values = gameController.pollAdc()
			#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
			#print(gameController.target_state)
			for i in range(0,targetCount):
				if values[i]>impactThreshold and gameController.target_state[i] is 1:
					gameController.target_state[i] = 2
					# TODO: code to change target color
					gv.lightController.getLights()[i].changeAll(0,0,255,1,True)
					# TODO: check if winner
					if sum(gameController.target_state[0:3]) is 6:
						gv.winner = 1
						return True
					elif sum(gameController.target_state[3:6]) is 6:
						gv.winner = 2
						return True
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
			retVal = gameController.checkLift()
			if retVal > 0:
				gv.penalty = retVal
				return True
			#setup button press monitoring here
			pass
	def checkLift():
		values = gameController.pollAdc()
		for i in range(6,8):
			if values[i] > 10.0 and values[i] < 1010.0:
				print("returning ",i-5,values[i])
				return i - 5
		return 0

# PINS FOR GAME PROFILE 1 (standard)
# 0,1,2 - Player 1 targets
# 3,4,5 - Player 2 targets
# 6,7 - Hand check










