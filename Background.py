import math
import pygame as py

class background:

	def __init__(self, width, height, image, screen):
		self.bg = py.image.load(image).convert()
		newScale = (1388, 628) # figure out how to compute		 FIX ME
		self.bg = py.transform.scale(self.bg, newScale)
		self.scroll = 0
		self.screen = screen
		self.tiles = math.ceil(width / self.bg.get_width()) + 1
	def drawBackground(self, scrollAmount):

		i = 0
		while (-self.tiles < i < self.tiles):
			self.screen.blit(self.bg, (self.bg.get_width() * i + self.scroll, 0))
			if scrollAmount <= 0:
				self.screen.blit(self.bg, (self.bg.get_width() * (i - 1) + self.scroll, 0))
				i += 1
			else:
				self.screen.blit(self.bg, (self.bg.get_width() * (i + 1) + self.scroll, 0))
				i -= 1




		# FRAME FOR SCROLLING
		self.scroll += scrollAmount

		# RESET THE SCROLL FRAME
		if abs(self.scroll) > self.bg.get_width():
			self.scroll = 0
