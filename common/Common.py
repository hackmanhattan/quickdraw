import pygame, sys
from pygame.locals import *

#initialize basic pygame lib including fonts
pygame.init()

class globalVars():
  #initialize global variables
  basicFont = pygame.font.SysFont(None, 72)
  musicIsOn = False
  musicPos = 0
  round_time = 0
  round_start_time = 0
  cur_elapsed = 0
  music_fadeout_time = 1500
  currentState = None
  round_start_effect = pygame.mixer.Sound('../audio/goodbadugly-whistle-long.wav')
  round_min = 4
  round_max = 11
  winner = 2
  penalty = 0
  basicfont = pygame.font.SysFont(None, 72)

  debug = True

  screen = pygame.display.set_mode((1600,900))
  clock = pygame.time.Clock()
  music = pygame.mixer.music

  gameStates = {}


  def loadMusic():
    globalVars.music.load("../audio/background_music.mp3")


#Global functions
def pauseMusic():
  print(globalVars.musicPos)
  globalVars.musicPos = globalVars.music.get_pos()
  print(globalVars.musicPos)
  globalVars.music.fadeout(globalVars.music_fadeout_time)

def unpauseMusic():	
  print(globalVars.musicPos)
  globalVars.music.play(-1, globalVars.musicPos/1000)

def changeState(index):
  print('testing')
  print(index)
  #print(globalVars.gameStates)
  globalVars.currentState.leave()
  globalVars.currentState = globalVars.gameStates[index]
  globalVars.currentState.enter()