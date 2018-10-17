import pygame, math
from common.Common import globalVars as gv

class Image:
	def __init__(self, name, image, pos_x, pos_y, draw):
		self.name = name
		self.image = pygame.image.load(image)
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.drawable = draw
		self.offsetX = 0
		self.offsetY = 0

	def draw(self, screen):
		if (self.drawable):
			screen.blit(self.image, ( (self.pos_x + self.offsetX), (self.pos_y + self.offsetY) ))
			#pygame.display.update()

class TextField:
	def __init__(self, name, text, pos_x, pos_y, draw, color=(0,0,0)):
		self.name = name
		self.text = text
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.drawable = draw
		self.color = color
		self.offsetX = 0
		self.offsetY = 0

	def draw(self, screen):
		if (self.drawable):
			texta = gv.basicFont.render(self.text,True, self.color)

			textrecta = texta.get_rect()
			textrecta.centerx = screen.get_rect().centerx + (self.pos_x + self.offsetX)
			textrecta.centery = screen.get_rect().centery + (self.pos_y + self.offsetY)
			screen.blit(texta,textrecta)
			#pygame.display.update()

