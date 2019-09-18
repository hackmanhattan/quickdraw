import pygame, math
from common.Drawable import Image, TextField
import common.AnimationController

class GameObject:
	def __init__(self, pos_x, pos_y, draw, image = None, text = None):
		self.image = image
		self.text = text
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.animations = []
		self.lights = []
		self.drawable = draw

	def update(self, deltaTime):
		for animate in self.animations:
			if animate.active:
				animate.tick(deltaTime)
				animate.animate(self)
		for light in self.lights:
			if light.active:
				light.tick(deltaTime)
				light.animate(self)
		if self.image:
			self.image.offsetX = self.pos_x
			self.image.offsetY = self.pos_y
		#Disabling this due to text getting screen center by default
		# TODO fix this
		#if self.text:
		#	self.text.offsetX = self.pos_x
		#	self.text.offsetY = self.pos_y

	def draw(self, screen):
		if self.drawable:
			if self.image:
				self.image.draw(screen)
			if self.text:
				self.text.draw(screen)

	def add_animation(self, animation_controller):
		self.animations.append(animation_controller)
	
	def add_light(self, light):
		self.lights.append(light)