import pygame
from random import randint, choice

#-------------------------------------------------#
# Class : Obstacle
#-------------------------------------------------#

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		elif type == 'snail':
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300
		elif type == 'Nightborne':
			Nightborne_1 = pygame.image.load('graphics/NightBorne.png').convert_alpha()
			Nightborne_2 = pygame.image.load('graphics/NightBorne_run.png').convert_alpha()
			self.frames = [Nightborne_1,Nightborne_2]
			y_pos = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6   #speed of obstacle coming towards the player TODO: Make it configurable i.e. start with slow speed and then increase it with difficulty level increases
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()