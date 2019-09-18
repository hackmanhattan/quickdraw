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
  max_framerate = 30
  round_min = 4
  round_max = 11
  winner = 2
  penalty = 0
  basicfont = pygame.font.SysFont(None, 72)

  debug = True
  screen_width = 1600
  screen_height = 900


  screen = pygame.display.set_mode((screen_width,screen_height))
  clock = pygame.time.Clock()
  music = pygame.mixer.music

  lightController = None
  gameStates = {}


  def loadMusic():
    globalVars.music.load("../audio/background_music.mp3")


#Global functions
def pauseMusic():
  globalVars.musicPos = globalVars.music.get_pos()
  globalVars.music.fadeout(globalVars.music_fadeout_time)

def unpauseMusic():	
  globalVars.music.play(-1, globalVars.musicPos/1000)

def changeState(index):
  print(index)
  #print(globalVars.gameStates)
  globalVars.currentState.leave()
  globalVars.currentState = globalVars.gameStates[index]
  globalVars.currentState.enter()