import pygame, math
from common.Common import globalVars as gv

class Image:
	def __init__(self, name, image, pos_x, pos_y, draw):
		self.name = name
		self.image = pygame.image.load(image)
		self.orig = self.image
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.drawable = draw
		self.offsetX = 0
		self.offsetY = 0
		size = self.image.get_size()
		self.center = (size[0]/2, size[1]/2)

	def draw(self, screen):
		if (self.drawable):
			size = self.image.get_size()
			#get the center of the image in case of rotation
			newPos = (
				(self.center[0] - (size[0]/2) ) + self.offsetX, 
				(self.center[1] - (size[1]/2) ) + self.offsetY
				)
			screen.blit(self.image, newPos)
	
	def rotate(self, angle):
		print(angle)
		self.image = pygame.transform.rotate(self.orig, -angle)

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
