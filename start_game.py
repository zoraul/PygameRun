import pygame
import os
import sqlite3
from sys import exit
from random import randint, choice

#----------------------- Class Player: Start--------------------------
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_run_1 = pygame.image.load('graphics/player/knight/player_run_1.png').convert_alpha()
		player_run_5 = pygame.image.load('graphics/player/knight/player_run_5.png').convert_alpha()
		player_run_10 = pygame.image.load('graphics/player/knight/player_run_10.png').convert_alpha()
		self.player_run = [player_run_1, player_run_5, player_run_10]

		player_jump_1 = pygame.image.load('graphics/player/knight/player_jump_1.png').convert_alpha()
		player_jump_2 = pygame.image.load('graphics/player/knight/player_jump_2.png').convert_alpha()
		player_jump_3 = pygame.image.load('graphics/player/knight/player_jump_3.png').convert_alpha()
		player_jump_4 = pygame.image.load('graphics/player/knight/player_jump_4.png').convert_alpha()
		player_jump_5 = pygame.image.load('graphics/player/knight/player_jump_5.png').convert_alpha()
		player_jump_6 = pygame.image.load('graphics/player/knight/player_jump_6.png').convert_alpha()
		player_jump_7 = pygame.image.load('graphics/player/knight/player_jump_7.png').convert_alpha()
		player_jump_8 = pygame.image.load('graphics/player/knight/player_jump_8.png').convert_alpha()
		player_jump_9 = pygame.image.load('graphics/player/knight/player_jump_9.png').convert_alpha()
		player_jump_10 = pygame.image.load('graphics/player/knight/player_jump_10.png').convert_alpha()

		self.player_jump = [player_jump_1, player_jump_2, player_jump_3, player_jump_4, player_jump_5, 
					  player_jump_6, player_jump_7, player_jump_8, player_jump_9, player_jump_10]
		
		self.player_index = 0
		self.image = self.player_run[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

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
#----------------------- Class Player: End --------------------------

#----------------------- Class Obstacle: Start --------------------------
class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

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
#----------------------- Class Obstacle: End --------------------------

#----------------------- Function display_score: Start ----------------
def display_higest_score():
	highestScoreRow = get_highest_score()
	hg_score_surf = test_font.render(f'Higest Score: {highestScoreRow}',False,'RED')
	hg_score_rect = hg_score_surf.get_rect(center = (400,20))
	screen.blit(hg_score_surf, hg_score_rect)
#----------------------- Function collision_sprite: End ----------------

#----------------------- Function display_score: Start ----------------
def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time
#----------------------- Function collision_sprite: End ----------------

#----------------------- Function collision_sprite: Start ----------------
def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True
#----------------------- Function collision_sprite: End ----------------

#----------------------- Function database_init: Start ----------------
def database_init():
	print("database_init - going to create/open db connection.....1")
	global dbConnection, cursor, highestScoreRow
	dbConnection = sqlite3.connect("database/pygameRun.db") # opening the database connection
	cursor = dbConnection.cursor()
	cursor.execute("create table if not exists higest_score(name text, score integer)")
	highestScoreRow = get_highest_score()
	print("database_init - created/opened db connection with higest_score table having value = ", highestScoreRow)
#----------------------- Function database_init: End ----------------

#----------------------- Function get_highest_score: Start ----------------
def get_highest_score():
	return cursor.execute("select * from higest_score where name = ?", (player_name,)).fetchone()
#----------------------- Function get_highest_score: End ----------------

#----------------------- Function update_score: Start ----------------
def update_score():
	retValue = False
	print("update_score - **score = ", score)
	highestScoreRow = get_highest_score()
	if highestScoreRow == None:
		print("*************** INSERT")
		cursor.execute("insert into higest_score(name, score) values(?,?)", (player_name, score))
		cursor.connection.commit()
	elif (isinstance(highestScoreRow[1], (int)) and highestScoreRow[1] < score):
		print("*************** UPDATE")
		cursor.execute("update higest_score set score = ? where name is ?", (score, player_name))
		cursor.connection.commit()
		retValue = True
	print(cursor.execute("select * from higest_score").fetchall())
	return retValue
#----------------------- Function update_score: End ----------------


#----------------------- Main program: Start ----------------
# Changing the current working directory
os.chdir('c:/Zorawar/PythonProjects/PygameRun') #NOTE: Change this path as per your project location
player_name = 'ZORAWAR' #static player name at the moment. TODO Input this from the user
database_init()
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Zorawar - run run and win!')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/player/knight/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Zorawar Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Hey, Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			print("**score = ", score)
			highestScoreUpdated = update_score()
			if highestScoreUpdated:
				print("You have broken the record and having higest score of ", score)
			dbConnection.close() # close the database connection
			exit()

		if game_active:
			if event.type == obstacle_timer:
				display_higest_score()
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				highestScoreUpdated = update_score()
				display_higest_score()
				if highestScoreUpdated:
					print("You have broken the record and having higest score of ", score)
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		display_higest_score()
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)
#----------------------- Main program: End ----------------