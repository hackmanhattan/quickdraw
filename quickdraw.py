import pygame, sys
from pygame.locals import *
import random
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


###################################
#       CLASS DEFINITIONS         #
###################################
class Drawable:
	def __init__(self, name, image, pos_x, pos_y, draw):
		self.name = name
		self.image = pygame.image.load(image)
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.drawable = draw

	def draw(self, screen):
		if (self.drawable):
			screen.blit(self.image, (self.pos_x, self.pos_y))
			#pygame.display.update()

class TextField:
	def __init__(self, name, text, pos_x, pos_y, draw):
		self.name = name
		self.text = text
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.drawable = draw

	def draw(self, screen):
		if (self.drawable):
			texta = basicfont.render(self.text,True, (0, 0, 0))

			textrecta = texta.get_rect()
			textrecta.centerx = screen.get_rect().centerx + self.pos_x
			textrecta.centery = screen.get_rect().centery + self.pos_y
			screen.blit(texta,textrecta)
			#pygame.display.update()


SPI_PORT = 0
SPI_DEVICE = 0

backgrounds = []
foregrounds = [None, Drawable("background_wait", "clint.png", 0,150, True ), None, None, None, None, None]

mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
 
pygame.init()
 
pygame.display.set_caption('Quickdraw by HackManhattan')
size = [1600, 900]
#size = [1280, 768]
#screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode(size, FULLSCREEN) 
signal_reads = 10
clock = pygame.time.Clock()
screen.fill((255, 255, 255))

basicfont = pygame.font.SysFont(None, 72)

color_font = (0, 0, 0)
color_bg = (255,255,255)

piezo_min = 50

# music definition
pygame.mixer.music.load("../audio/bg.mp3")

# effects definition
effect = pygame.mixer.Sound('../audio/Zen_Buddhist_Temple_Bell-SoundBible.com-331362457.wav')
round_start_effect = pygame.mixer.Sound('../audio/goodbadugly-whistle-long.wav')
draw_sound = pygame.mixer.Sound('../audio/draw.wav')
timeout_sound = pygame.mixer.Sound('../audio/youdone.wav')

reset_idx = 5
round_min = 4
round_max = 8

round_start = False
round_start_time = 0
round_timeout = 30

music_fadeout_time = 1500
#screen images
titlescreen = pygame.image.load('quickdraw_title_b.jpg')
wait_screen = pygame.image.load('quickdraw_wait.jpg')
draw_screen = pygame.image.load('quickdraw_draw.jpg')

#Setup the backgrounds

# 0 game initialized
backgrounds.append(Drawable("background_title", "quickdraw_title_b.jpg", 0,0, True ))
# 1 round started
backgrounds.append(Drawable("background_wait", "quickdraw_wait.jpg", 0,0, True ))
# 2 ready for fire
backgrounds.append(Drawable("background_draw", "quickdraw_draw.jpg", 0,0, True ))
# 3 winner 
backgrounds.append(Drawable("background_p2win", "quickdraw_p2win.jpg", 0,0, True ))
# 4 penalty
backgrounds.append(Drawable("background_penalty", "quickdraw_penalty.jpg", 0,0, True ))
# 5 timeout
backgrounds.append(Drawable("background_timeout", "quickdraw_timeout.jpg", 0,0, True ))
# 6 player1 winner
backgrounds.append(Drawable("background_p1win", "quickdraw_p1win.jpg", 0,0, True ))


musicpos = 0

def pause_music():
	musicpos = pygame.mixer.music.get_pos()
	pygame.mixer.music.fadeout(music_fadeout_time)

def unpause_music():
	pygame.mixer.music.play(musicpos)

def readadc():
	values = [0]*8
	for j in range(0,signal_reads):
		for i in range(8):
			values[i] +=  mcp.read_adc(i)
	for i in range(0,8):
		values[i] = values[i] / (signal_reads *1.0)
	return values

def get_winner(values):
	# TODO: should read for targets
	for i in range(2,4):
		if values[i] > piezo_min:
			return i-2
	return -1

def space_pressed(values):
	print("yo",values)
	if values[reset_idx] >= 1022:
		print("space_pressed")
		time.sleep(0.25)
		return True
	return False

def gamestart():
	return True

def render_fire(time_elapsed):
	return True

def render_penalty(tgtplayer,count,game_state,texts):
	texts[game_state].text = "Player " + str(tgtplayer+1)
	

def quit_game():
	pygame.quit()
	sys.exit()

def render_round_start():
	return True

def player_win(tgtplayer,tgttime,game_state,texts):
	result = "Time elapsed " + str(tgttime) + " seconds"
	texts[game_state].text = result
	

def gun_picked_up(values):
	for i in range(2):
		if values[i] < 999:
			return i
	return -1

# random start time
clock.tick(120)

def changeState(state):
	if (game_state != state):
		backgrounds[game_state].drawable = False
		game_state = state
		backgrounds[game_state].drawable = True



def main():
	round_time = 0
	round_start_time = 0
	menu_timeout = 0
	

	game_state = 0 #flag for game state
	
	# 0 game initialized
	# 1 round started
	# 2 ready for fire
	# 3 player 2 winner 
	# 4 penalty
	# 5 timeout
	# 6 player 1 winner
	game_win = {}
	penalty = {}
	# start music
	music_is_on = False

	texts = [None, None, None, TextField("p2win", "test", 200, 400, True),  TextField("penalty", "test", 350, -60, True), None, None]

	while True:

		#Render all the drawables on a new screen
		screen.fill((255,255,255))
		#for drawable in backgrounds:
		#	drawable.draw(screen)

		backgrounds[game_state].draw(screen)

		if foregrounds[game_state]:
			foregrounds[game_state].draw(screen)

		if texts[game_state]:
			texts[game_state].draw(screen)

		pygame.display.update()

		cur_input = readadc()
		#print(cur_input)
		if space_pressed(cur_input):
			if game_state is 0:
				#pygame.mixer.music.fadeout(music_fadeout_time)
				#pygame.mixer.music.pause()
				pause_music()
				round_start_effect.play()
				game_state = 1

				#reset clint for his slow travel
				foregrounds[1].pos_x = 10

				round_time = random.randint(round_min, round_max)
				round_start_time = time.time()
			elif game_state in [3,4,5,6]:
				game_state = 0
				penalty = {}
				winner = {}
				music_is_on = True
				#pygame.mixer.music.unpause()
				unpause_music()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					quit_game()
				elif event.key == K_SPACE and game_state is 0:
					pygame.mixer.music.pause()
					#pygame.mixer.music.fadeout(music_fadeout_time)
					round_start_effect.play()					
					game_state = 1
					
					#reset clint for his slow travel
					foregrounds[1].pos_x = 10

					round_time = random.randint(2,6)
					round_start_time = time.time()
				elif event.key == K_SPACE and game_state in [3,4,5,6]:
					# winner to new game
					game_state = 0
					# reset penalty and winner
					penalty = {}
					winner = {}
					music_is_on = True
					pygame.mixer.music.unpause()

		if game_state is 0:
			gamestart()
			if not music_is_on:
				music_is_on = True
				pygame.mixer.music.play()

		elif game_state is 1:
			render_round_start()
			cur_elapsed = time.time() - round_start_time

			#move clint across the screen slowly
			foregrounds[1].pos_x += 1
			if gun_picked_up(cur_input) != -1:
				penalty["player"] = gun_picked_up(cur_input)
				if "count" in penalty:
					penalty["count"] += 1
					game_state = 4
					menu_timeout = time.time()
				else:
					penalty["count"] = 1

			print(cur_elapsed,"time passed")
			if cur_elapsed > round_time:
				round_start_effect.stop()
				#effect.play()
				game_state = 2
				draw_sound.play()
				round_start_time = time.time()
				music_is_on = False

		elif game_state is 2:
			cur_elapsed = time.time() - round_start_time
			if cur_elapsed > round_timeout:
				menu_timeout = time.time()
				game_state = 5
				timeout_sound.play()
			render_fire(time.time() - round_start_time)
			if get_winner(cur_input) != -1:
				if get_winner(cur_input) == 0:
					game_state = 6
				else:
					game_state = 3
				menu_timeout = time.time()
				game_win["player"] = get_winner(cur_input)
				game_win["time"] = time.time() - round_start_time

		elif game_state in [3,6]:
			player_win(game_win["player"],game_win["time"],game_state,texts)
			#start the timer to go back to the start screen
			cur_elapsed = time.time() - menu_timeout
			if cur_elapsed > round_timeout:
				#go back to the start screen
				game_state = 0
				unpause_music()

		elif game_state is 4:
			render_penalty(penalty["player"],penalty["count"],game_state,texts)
			#start the timer to go back to the start screen
			cur_elapsed = time.time() - menu_timeout
			if cur_elapsed > round_timeout:
				#go back to the start screen
				game_state = 0
				unpause_music()

		elif game_state is 5:
			#start the timer to go back to the start screen
			cur_elapsed = time.time() - menu_timeout
			if cur_elapsed > round_timeout:
				#go back to the start screen
				game_state = 0
				unpause_music()

		

main()