import pygame, sys
from pygame.locals import *
import random
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT = 0
SPI_DEVICE = 0

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

piezo_min = 300

# music definition
pygame.mixer.music.load("Dj_Okawari_Kaleidoscope_Full.mp3")

# effects definition
effect = pygame.mixer.Sound('Zen_Buddhist_Temple_Bell-SoundBible.com-331362457.wav')
round_start_effect = pygame.mixer.Sound('goodbadugly-whistle-long.wav')

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
	screen.blit(titlescreen,(0,0))
	pygame.display.update()

def render_fire(time_elapsed):
	screen.fill(color_bg)
	screen.blit(draw_screen, (0,0))
	pygame.display.update()

def render_penalty(tgtplayer,count):
	cur_text = "PENALTY FOR " + str(tgtplayer)
	cur_text = basicfont.render(cur_text, True, color_font, color_bg)
	cur_textrect = cur_text.get_rect()
	cur_textrect.centerx = screen.get_rect().centerx
	cur_textrect.centery = screen.get_rect().centery-100

	textb = str(count) + " foul"
	textb = basicfont.render(textb, True, color_font, color_bg)
	textbrect = textb.get_rect()
	textbrect.centerx = screen.get_rect().centerx
	textbrect.centery = screen.get_rect().centery
	screen.fill(color_bg)

	textc = 'Press SPACE to continue.'
	textc = basicfont.render(textc, True, color_font, color_bg)
	textrectc = textc.get_rect()
	textrectc.centerx = screen.get_rect().centerx
	textrectc.centery = screen.get_rect().centery + 100

	screen.blit(cur_text, cur_textrect)
	screen.blit(textb,textbrect)
	screen.blit(textc,textrectc)
	pygame.display.update()

def render_timeout():
	texta = "No Winner!"
	texta = basicfont.render(texta,True,color_font,color_bg)
	textrecta = texta.get_rect()
	textrecta.centerx = screen.get_rect().centerx
	textrecta.centery = screen.get_rect().centery

	screen.fill(color_bg)
	screen.blit(texta,textrecta)
	pygame.display.update()


def quit_game():
	pygame.quit()
	sys.exit()


def player_win(tgtplayer,tgttime):
        tgtstr = 'NO WINNER'
        cur_text = basicfont.render(tgtstr, True, color_font,color_bg)
        cur_textrect = cur_text.get_rect()
        cur_textrect.centerx = screen.get_rect().centerx
        cur_textrect.centery = screen.get_rect().centery - 100
        textc = 'Press SPACE to continue.'
        textc = basicfont.render(textc, True, color_font, color_bg)
        textrectc = textc.get_rect()
        textrectc.centerx = screen.get_rect().centerx
        textrectc.centery = screen.get_rect().centery + 100

        screen.fill((255, 255, 255))
        screen.blit(cur_text, cur_textrect)
        screen.blit(textc, textrectc)
	pygame.display.update()


def render_round_start():
	screen.blit(wait_screen,(0,0))
	pygame.display.update()

def player_win(tgtplayer,tgttime):
	tgtstr = 'Player ' + str(tgtplayer) + ' WINS'
	cur_text = basicfont.render(tgtstr, True, color_font,color_bg)
	cur_textrect = cur_text.get_rect()
	cur_textrect.centerx = screen.get_rect().centerx
	cur_textrect.centery = screen.get_rect().centery - 100

	result = "Time elapsed " + str(tgttime) + " seconds"
	text_time = basicfont.render(result, True, color_font,color_bg)
	text_time_rect = text_time.get_rect()
	text_time_rect.centerx = screen.get_rect().centerx
	text_time_rect.centery = screen.get_rect().centery

	textc = 'Press SPACE to continue.'
	textc = basicfont.render(textc, True, color_font, color_bg)
	textrectc = textc.get_rect()
	textrectc.centerx = screen.get_rect().centerx
	textrectc.centery = screen.get_rect().centery + 100

	screen.fill((255, 255, 255))
	screen.blit(cur_text, cur_textrect)
	screen.blit(text_time, text_time_rect)
	screen.blit(textc, textrectc)
	pygame.display.update()

def gun_picked_up(values):
	for i in range(2):
		if values[i] < 999:
			return i
	return -1

# random start time
clock.tick(120)

def main():
	round_time = 0
	round_start_time = 0
	game_state = 0 #flag for game state
	# 0 game initialized
	# 1 round started
	# 2 ready for fire
	# 3 winner 
	# 4 penalty
	# 5 timeout
	game_win = {}
	penalty = {}
	# start music
	music_is_on = False
	while True:
		cur_input = readadc()
		#print(cur_input)
		if space_pressed(cur_input):
			if game_state is 0:
				#pygame.mixer.music.fadeout(music_fadeout_time)
				pygame.mixer.music.pause()
				round_start_effect.play()
				game_state = 1
				round_time = random.randint(round_min, round_max)
				round_start_time = time.time()
			elif game_state in [3,4,5]:
				game_state = 0
				penalty = {}
				winner = {}
				music_is_on = True
                                pygame.mixer.music.unpause()
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
					round_time = random.randint(2,6)
					round_start_time = time.time()
				elif event.key == K_SPACE and game_state in [3,4,5]:
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
			if gun_picked_up(cur_input) != -1:
				penalty["player"] = get_winner(cur_input)
				if "count" in penalty:
					penalty["count"] += 1
					game_state = 4
				else:
					penalty["count"] = 1

			print(cur_elapsed,"time passed")
			if cur_elapsed > round_time:
				round_start_effect.stop()
				effect.play()
				game_state = 2
				round_start_time = time.time()
				music_is_on = False
		elif game_state is 2:
			cur_elapsed = time.time() - round_start_time
			if cur_elapsed > round_timeout:
				game_state = 5
			render_fire(time.time() - round_start_time)
			if get_winner(cur_input) != -1:
				game_state = 3
				game_win["player"] = get_winner(cur_input)
				game_win["time"] = time.time() - round_start_time
		elif game_state is 3:
			player_win(game_win["player"],game_win["time"])
		elif game_state is 4:
			render_penalty(penalty["player"],penalty["count"])
		elif game_state is 5:
			render_timeout()

main()
