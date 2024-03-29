import pygame

#-------------------------------------------------#
# Class : Player
#-------------------------------------------------#


class Player(pygame.sprite.Sprite):
	LEFT_BONDARY, RIGHT_BOUNDARY = 5, 750
	
	def __init__(self):
		super().__init__()
		player_run_1 = pygame.image.load('resources/graphics/player/knight/player_run_1.png').convert_alpha()
		player_run_5 = pygame.image.load('resources/graphics/player/knight/player_run_5.png').convert_alpha()
		player_run_10 = pygame.image.load('resources/graphics/player/knight/player_run_10.png').convert_alpha()
		self.player_run = [player_run_1, player_run_5, player_run_10]

		player_jump_1 = pygame.image.load('resources/graphics/player/knight/player_jump_1.png').convert_alpha()
		player_jump_2 = pygame.image.load('resources/graphics/player/knight/player_jump_2.png').convert_alpha()
		player_jump_3 = pygame.image.load('resources/graphics/player/knight/player_jump_3.png').convert_alpha()
		player_jump_4 = pygame.image.load('resources/graphics/player/knight/player_jump_4.png').convert_alpha()
		player_jump_5 = pygame.image.load('resources/graphics/player/knight/player_jump_5.png').convert_alpha()
		player_jump_6 = pygame.image.load('resources/graphics/player/knight/player_jump_6.png').convert_alpha()
		player_jump_7 = pygame.image.load('resources/graphics/player/knight/player_jump_7.png').convert_alpha()
		player_jump_8 = pygame.image.load('resources/graphics/player/knight/player_jump_8.png').convert_alpha()
		player_jump_9 = pygame.image.load('resources/graphics/player/knight/player_jump_9.png').convert_alpha()
		player_jump_10 = pygame.image.load('resources/graphics/player/knight/player_jump_10.png').convert_alpha()
		
		self.player_jump = [player_jump_1, player_jump_2, player_jump_3, player_jump_4, player_jump_5, 
					  player_jump_6, player_jump_7, player_jump_8, player_jump_9, player_jump_10]
		
		#TODO Future implementation of Attack feature
		self.player_dead = pygame.image.load('resources/graphics/player/knight/player_bend_1.png').convert_alpha()
		
		self.player_index = 0
		self.image = self.player_run[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0
		self.player_lives = 3
		self.player_speed = 5
		self.jump_sound = pygame.mixer.Sound('resources/audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP] and self.rect.bottom >= 300:
			self.gravity = -15
			self.jump_sound.play()
		if keys[pygame.K_RIGHT]:
			#check if the movement is within the boundary and only then allow it
			if (self.rect.x + self.player_speed) < self.__class__.RIGHT_BOUNDARY:
				self.rect.x += self.player_speed			
		if keys[pygame.K_LEFT]:
			#Tcheck if the movement is within the boundary and only then allow it
			if (self.rect.x + self.player_speed) > self.__class__.LEFT_BONDARY:
				self.rect.x -= self.player_speed
		#if keys[pygame.K_SPACE]:
			#TODO change the player in the attack animation

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image =  self.player_jump[0]
			
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_run):self.player_index = 0
			self.image = self.player_run[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()