# move pan

import pygame

class Pan:
	"""Pan move in display"""
	
	pan_width = 140  # Pan width
	pan_height = 70  # Pan height

	def __init__(self, x, y, screen, pan):
		"""initialization object"""
		self.x = x
		self.y = y
		self.screen = screen
		self.pan = pan

	def move(self):
		"""Get mouse coords"""
		x, y = pygame.mouse.get_pos() 
		x, y = self.check_position(x, y)

		self.move_x = x
		self.move_y = y

		return self.move_x, self.move_y

	def check_position(self, x, y):
		"""Check mouse coords that pan dont out with display"""
		if x - self.pan_width / 2 < 0:
			x = 0 + self.pan_width / 2
		elif x + self.pan_width / 2 > 1920:
			x = 1920 - self.pan_width / 2

		if y < 300 + self.pan_height / 2:
			y = 300 + self.pan_height / 2
		elif y + self.pan_height / 2 > 1080:
			y = 1080 - self.pan_height / 2 

		return x, y

