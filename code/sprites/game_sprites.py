import pygame
import application_log
from random import randint, choice
from enum import IntEnum
from sprites import constants 

logger = application_log.logger_config(__name__)

def _get_Enemy_Sprite(type):
		if (type == constants.ENEMY_TYPE_FLY):
			return EnemyFly()
		elif type == constants.ENEMY_TYPE_SNAIL:
			return EnemySnail()
		elif type == constants.ENEMY_TYPE_NIGHTBORNE:
			return EnemyNightborne()
		elif type == constants.ENEMY_TYPE_ALIEN:
			return EnemyAlien()
		elif type == constants.POWER_UP_SPRITE:
			return PowerUpSprite()
		else:
			logger.error('Enemy sprite of the given type {type} cannot be created.'.format(type=repr(type)))
			raise ValueError('Enemy sprite of the given type {type} cannot be created.'.format(type=repr(type)))


#-------------------------------------------------#
#
# Class : PowerUpSprite 
# Parent Class : pygame.sprite.Sprite (pygame libray)
#
#-------------------------------------------------#
class PowerUpSprite(pygame.sprite.Sprite):
	IMAGE_1 = 'resources/graphics/powerup/power_up_1.png'
	IMAGE_2 = 'resources/graphics/powerup/power_up_2.png'
	DEFAULT_SPEED = 5
	Y_POSITION = 150

	def __init__(self):
		super().__init__()
		self.type = constants.ENEMY_TYPE_NIGHTBORNE
		self.speed = self.DEFAULT_SPEED
		img_1 = pygame.image.load(self.IMAGE_1).convert_alpha()
		img_2 = pygame.image.load(self.IMAGE_2).convert_alpha()
		self.frames = [img_1,img_2]
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100), self.Y_POSITION))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= self.speed   
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

#-------------------------------------------------#
#
# Class : EnemySprite 
# Parent Class : pygame.sprite.Sprite (pygame libray)
#
#-------------------------------------------------#
class EnemySprite(pygame.sprite.Sprite):

	game_level = "Easy"
	speed = 6
	type = 'EnemySprite'
	
	class Level(IntEnum):
		EASY = 2000
		MEDIUM = 1500
		HARD = 1000
		HARDEST = 500

	def __init__(self):
		super().__init__()

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= self.speed   
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()


#-------------------------------------------------#
#
# Class : EnemyFly 
# Parent Class : EnemySprite
#
#-------------------------------------------------#
class EnemyFly(EnemySprite):
	IMAGE_1 = 'resources/graphics/fly/fly1.png'
	IMAGE_2 = 'resources/graphics/fly/fly2.png'
	DEFAULT_SPEED = 4
	Y_POSITION = 215


	def __init__(self):
		super().__init__()
		self.type = constants.ENEMY_TYPE_FLY
		self.speed = self.DEFAULT_SPEED
		fly_1 = pygame.image.load(self.IMAGE_1).convert_alpha()
		fly_2 = pygame.image.load(self.IMAGE_2).convert_alpha()
		self.frames = [fly_1,fly_2]
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100), self.Y_POSITION))


#-------------------------------------------------#
#
# Class : EnemySnail 
# Parent Class : EnemySprite
#
#-------------------------------------------------#
class EnemySnail(EnemySprite):
	IMAGE_1 = 'resources/graphics/snail/snail1.png'
	IMAGE_2 = 'resources/graphics/snail/snail2.png'
	DEFAULT_SPEED = 6
	Y_POSITION = 300

	def __init__(self):
		super().__init__()
		self.type = constants.ENEMY_TYPE_SNAIL
		self.speed = self.DEFAULT_SPEED
		fly_1 = pygame.image.load(self.IMAGE_1).convert_alpha()
		fly_2 = pygame.image.load(self.IMAGE_2).convert_alpha()
		self.frames = [fly_1,fly_2]
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100), self.Y_POSITION))


#-------------------------------------------------#
#
# Class : EnemyNightborne 
# Parent Class : EnemySprite
#
#-------------------------------------------------#
class EnemyNightborne(EnemySprite):
	IMAGE_1 = 'resources/graphics/NightBorne.png'
	IMAGE_2 = 'resources/graphics/NightBorne_run.png'
	DEFAULT_SPEED = 8
	Y_POSITION = 300

	def __init__(self):
		super().__init__()
		self.type = constants.ENEMY_TYPE_NIGHTBORNE
		self.speed = self.DEFAULT_SPEED
		fly_1 = pygame.image.load(self.IMAGE_1).convert_alpha()
		fly_2 = pygame.image.load(self.IMAGE_2).convert_alpha()
		self.frames = [fly_1,fly_2]
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100), self.Y_POSITION))




#-------------------------------------------------#
#
# Class : EnemyAlien 
# Parent Class : EnemySprite
#
#-------------------------------------------------#
class EnemyAlien(EnemySprite):
	IMAGE_1 = 'resources/graphics/alien/alien1.png'
	IMAGE_2 = 'resources/graphics/alien/alien2.png'
	IMAGE_3 = 'resources/graphics/alien/alien3.png'
	IMAGE_4 = 'resources/graphics/alien/alien4.png'
	IMAGE_5 = 'resources/graphics/alien/alien5.png'
	IMAGE_6 = 'resources/graphics/alien/alien6.png'
	DEFAULT_SPEED = 2
	Y_POSITION = 300

	def __init__(self):
		super().__init__()
		self.type = constants.ENEMY_TYPE_SNAIL
		self.speed = self.DEFAULT_SPEED
		img_1 = pygame.image.load(self.IMAGE_1).convert_alpha()
		img_2 = pygame.image.load(self.IMAGE_2).convert_alpha()
		img_3 = pygame.image.load(self.IMAGE_3).convert_alpha()
		img_4 = pygame.image.load(self.IMAGE_4).convert_alpha()
		img_5 = pygame.image.load(self.IMAGE_5).convert_alpha()
		img_6 = pygame.image.load(self.IMAGE_6).convert_alpha()
		self.frames = [img_1,img_2, img_3, img_4, img_5, img_6]
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100), self.Y_POSITION))


