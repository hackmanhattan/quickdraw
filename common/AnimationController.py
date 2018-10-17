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
		delta_x = abs(self.start_x - self.target_x) / self.time
		delta_y = abs(self.start_y - self.target_y) / self.time

		self.cur_x += delta_x * deltaTime
		self.cur_y += delta_y * deltaTime

	def get_x(self):
		return self.cur_x

	def get_y(self):
		return self.cur_y
