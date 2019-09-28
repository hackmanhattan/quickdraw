import pygame
import time

class AnimationController:
	def __init__(self, start_x, start_y, target_x, target_y, time, active=False):
		self.start_x = start_x
		self.start_y = start_y
		self.target_x = target_x
		self.target_y = target_y
		self.time = time
		self.cur_x = start_x
		self.cur_y = start_y
		self.active = active

	def tick(self, deltaTime):
		if self.cur_x >= self.target_x:
			self.active = False
		delta_x = abs(self.start_x - self.target_x) / (self.time / 1000)
		delta_y = abs(self.start_y - self.target_y) / (self.time / 1000)

		self.cur_x += delta_x * deltaTime
		self.cur_y += delta_y * deltaTime

	def get_x(self):
		return self.cur_x

	def get_y(self):
		return self.cur_y


class TranslationController:
	def __init__(self, start_x, start_y, target_x, target_y, time, active=False):
		self.start_x = start_x
		self.start_y = start_y
		self.target_x = target_x
		self.target_y = target_y
		self.time = time
		self.cur_x = start_x
		self.cur_y = start_y
		self.active = active

	def tick(self, deltaTime):
		if self.cur_x >= self.target_x:
			self.active = False
		delta_x = abs(self.start_x - self.target_x) / (self.time / 1000)
		delta_y = abs(self.start_y - self.target_y) / (self.time / 1000)

		self.cur_x += delta_x * deltaTime
		self.cur_y += delta_y * deltaTime

	def get_x(self):
		return self.cur_x

	def get_y(self):
		return self.cur_y

	def animate(self, targetObj):
		#class functionality
		targetObj.pos_x = self.cur_x
		targetObj.pos_y = self.cur_y
		pass

class RotationController:
	def __init__(self, start_angle, target_angle, time, active=False):
		self.start_angle = start_angle
		self.target_angle = target_angle
		self.current_angle = self.start_angle
		self.time = time
		self.active = active

	def tick(self, deltaTime):
		if self.current_angle < self.target_angle:
			deltaAngle = abs(self.start_angle - self.target_angle) / (self.time / 1000)
			cur_angle = deltaAngle * deltaTime
			if (self.current_angle + cur_angle > self.target_angle):
				self.current_angle = self.target_angle
			else:
				self.current_angle += deltaAngle * deltaTime
		else:
			self.active = False

	def get_angle(self):
		return self.current_angle

	def animate(self, targetObj):
		#class functionality
		targetObj.image.rotate(self.current_angle)
		pass

class OpacityController:
	def __init__(self, start_alpha, target_alpha, timer_count, active=False):
		self.start_alpha = start_alpha
		self.current_alpha = start_alpha
		self.target_alpha = target_alpha
		self.start_time = time.time()
		self.current_time = time.time()
		self.target_time = time.time() + timer_count
		self.active = active

	def tick(self, deltaTime):
		if (self.current_time >= self.target_time):
			self.active = False

		self.current_time += deltaTime
		if (self.start_alpha < self.target_alpha):
			direction = 'fadeIn'
		else:
			direction = 'fadeOut'

		if (direction == 'fadeIn'):
			self.current_alpha = self.target_alpha - (self.timeRemaining() / self.totalTime())
			if self.current_alpha > self.target_alpha:
				self.current_alpha = self.target_alpha
		else:
			self.current_alpha = self.timeRemaining() / self.totalTime()
			if self.current_alpha < self.target_alpha:
				self.current_alpha = self.target_alpha # - 0.01

	def animate(self, targetObj):
		if targetObj.image.drawable == False:
			targetObj.image.drawable = True
		targetObj.image.image.set_alpha(255 * self.current_alpha)
		pass

	def timeRemaining(self):
		return self.target_time - self.current_time
		#Get the total time the animation was set for
	def totalTime(self):
		return self.target_time - self.start_time	

	def get_alpha(self):
		return self.current_alpha
		