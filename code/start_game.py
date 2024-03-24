import pygame
import os
import sqlite3
from sys import exit
from random import randint, choice

from sprites.constants import *
import sprites.game_sprites as game_sprites
import player.player as myplayer
import application_log

logger = application_log.logger_config(__name__)


def Main():
	WIDTH, HEIGHT = 800, 400
	clock = pygame.time.Clock()
	WORKING_DIR = 'C:/GitHub/PygameRun' #NOTE: Change this path as per your project location

	#------------------- Function: display_score ----------------
	# Displays the hightest score on the screen
	def display_higest_score():
		highestScoreRow = get_highest_score()
		hg_score_surf = game_font.render(f'Higest Score: {highestScoreRow}',False,'RED')
		hg_score_rect = hg_score_surf.get_rect(center = (400,20))
		screen.blit(hg_score_surf, hg_score_rect)

	#------------------- Function: display_score ----------------
	# Displays the current score of the player
	def display_score():
		current_time = int(pygame.time.get_ticks() / 1000) - start_time
		score_surf = game_font.render(f'Score: {current_time}',False,(64,64,64))
		score_rect = score_surf.get_rect(center = (400,50))
		screen.blit(score_surf,score_rect)
		return current_time

	#------------------- Function: display_lives ----------------
	# Displays the number of lives of the player
	def display_lives():
		lives_surf = game_font.render(f'Lives: {player.sprite.player_lives}',False,(64,64,64))
		lives_rect = lives_surf.get_rect(center = (600,50))
		screen.blit(lives_surf, lives_rect)

	#------------------- Function: display_game_level ----------------
	# Displays the game's difficulty level
	def display_game_level():
		level_surf = game_font.render(f'Level: {game_sprites.EnemySprite.game_level}',False,(64,64,64))
		level_rect = level_surf.get_rect(center = (200,50))
		screen.blit(level_surf, level_rect)

	#------------------- Function: collision_sprite ----------------
	# Checks if sprite collides with enemy and return true/false
	def collision_sprite():
		if pygame.sprite.spritecollide(player.sprite, enemy_group, False):
			logger.debug('collided with enemy group...')
			enemy_group.empty()
			player.sprite.player_lives -= 1
			player.sprite.image = player.sprite.player_dead
			game_active = False
			logger.debug("player lives = %s", player.sprite.player_lives)
		elif pygame.sprite.spritecollide(player.sprite, power_up, False):
			logger.debug('collided with power up sprite...')
			player.sprite.player_lives += 1
			logger.debug("player lives = %s", player.sprite.player_lives)
			power_up.empty()

	#------------------- Function: database_init ----------------
	# Initialise the database tables, connection, etc
	def database_init():
		logger.debug("database_init - going to create/open db connection...1")
		global dbConnection, cursor, highestScoreRow
		dbConnection = sqlite3.connect("database/pygameRun.db")
		cursor = dbConnection.cursor()
		cursor.execute("create table if not exists higest_score(name text, score integer)")
		highestScoreRow = get_highest_score()
		logger.debug("database_init - created/opened db connection with higest_score table having value = %s", highestScoreRow)

	#------------------- Function: get_personal_highest_score ----------------
	# Utility function to get the player's personal highest score from the database
	def get_personal_highest_score():
		return cursor.execute("select * from higest_score where name = ?", (player_name,)).fetchone()

	#------------------- Function: get_highest_score ----------------
	# Utility function to get the higest score from the database
	def get_highest_score():
		return cursor.execute("select * from higest_score where score = (select max(score) from higest_score)").fetchone()

	#------------------- Function: update_score ----------------
	# Insert or Update the score of current player in the database
	def update_score():
		retValue = False
		logger.debug("update_score - score = %s", score)
		personalhighestScoreRow = get_personal_highest_score()
		if personalhighestScoreRow == None:
			logger.debug("No existing record exist: INSERT the record in the database")
			cursor.execute("insert into higest_score(name, score) values(?,?)", (player_name, score))
			cursor.connection.commit()
		elif (isinstance(personalhighestScoreRow[1], (int)) and personalhighestScoreRow[1] < score):
			logger.debug("Existing record found: UPDATE the record in the database")
			cursor.execute("update higest_score set score = ? where name is ?", (score, player_name))
			cursor.connection.commit()
			retValue = True
		logger.debug('Players found in the database and their score: %s', cursor.execute("select * from higest_score").fetchall())
		return retValue

	#------------------- Function: update_game_level ----------------
	# updates the game's difficulty level
	def update_game_level():
		if score > 30:
			pygame.time.set_timer(obstacle_timer, int(game_sprites.EnemySprite.Level.HARDEST))
			game_sprites.EnemySprite.game_level = game_sprites.EnemySprite.Level.HARDEST.name
		elif score > 20:
			pygame.time.set_timer(obstacle_timer, int(game_sprites.EnemySprite.Level.HARD))
			game_sprites.EnemySprite.game_level = game_sprites.EnemySprite.Level.HARD.name
		elif score > 10:
			pygame.time.set_timer(obstacle_timer, int(game_sprites.EnemySprite.Level.MEDIUM))
			game_sprites.EnemySprite.game_level = game_sprites.EnemySprite.Level.MEDIUM.name
		else:
			pygame.time.set_timer(obstacle_timer, int(game_sprites.EnemySprite.Level.EASY))
			game_sprites.EnemySprite.game_level = game_sprites.EnemySprite.Level.EASY.name
			
	#------------------- Function: show_title_screen ----------------
	# shows the 'Title Screen'
	def show_title_screen():
		player_stand = pygame.image.load('resources/graphics/player/knight/player_stand.png').convert_alpha()
		player_stand = pygame.transform.rotozoom(player_stand,0,2)
		player_stand_rect = player_stand.get_rect(center = (400,200))
		game_name = game_font.render(player_name + ' Runner',False,(111,196,169))
		game_name_rect = game_name.get_rect(center = (400,80))
		game_message = game_font.render('Hey, Press space to run',False,(111,196,169))
		game_message_rect = game_message.get_rect(center = (400,330))

		screen.fill((94,129,162))
		screen.blit(player_stand, player_stand_rect)
		screen.blit(game_name,game_name_rect)
		screen.blit(game_message,game_message_rect)

	#------------------- Function: show_game_end_screen ----------------
	# shows the 'Game End Screen'
	def show_game_end_screen():
		player_stand = pygame.image.load('resources/graphics/player/knight/player_stand.png').convert_alpha()
		player_stand = pygame.transform.rotozoom(player_stand,0,2)
		player_stand_rect = player_stand.get_rect(center = (400,200))
		game_name = game_font.render(player_name + ' Runner',False,(111,196,169))
		game_name_rect = game_name.get_rect(center = (400,80))
		score_message = game_font.render(f'Your score: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)
		restart_message = game_font.render(f'Press space to restart a new game',False,(111,196,169))
		restart_message_rect = restart_message.get_rect(center = (400,380))

		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)
		screen.blit(score_message, score_message_rect)
		screen.blit(restart_message, restart_message_rect)

	#------------------- Function: show_play_screen ----------------
	# shows the 'Play Screen'
	def show_play_screen():
		sky_surface = pygame.image.load('resources/graphics/Sky.png').convert()
		ground_surface = pygame.image.load('resources/graphics/ground.png').convert()
		
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,300))
		display_higest_score()
		display_lives()
		display_game_level()
		update_player_score(display_score())
		
		player.draw(screen)
		player.update()

		enemy_group.draw(screen)
		enemy_group.update()
		power_up.draw(screen)
		power_up.update()

		collision_sprite()

	#------------------- Function: update_player_score ----------------
	# Update the score
	def update_player_score(s):
		global score
		score = s

	# shows the 'Play Screen'
	def input_player_name():
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

				elif event.type == pygame.KEYDOWN:

					if event.key == pygame.K_BACKSPACE:
						print('*************** Player name BEFORE: ', player_name)
						player_name = player_name[:-1]
						print('*************** Player name AFTER: ', player_name)
					elif event.key == pygame.K_RETURN:
						print("---------------------Pressed Enter")
						return player_name
					else:
						print('################ Player name BEFORE: ', player_name)
						player_name += event.unicode
						print('################ Player name AFTER: ', player_name)

			screen.fill(BLACK)

			input_surface = game_font.render(player_name, True, WHITE)
			screen.blit(input_surface, (10, 20))

			pygame.display.flip()


#------------------- Main program ----------------

	# Changing the current working directory
	os.chdir(WORKING_DIR)

	is_playername_valid = False
	while(not is_playername_valid):
		player_name = input("Enter your name: ")
		if(player_name != ''):
			is_playername_valid = True
		else:
			print("Invalid name: name cannot be empty.")

	global game_font
	global bg_music 

	pygame.init()
	database_init()

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(player_name + ' - run run and win!')
	clock = pygame.time.Clock()
	game_font = pygame.font.Font('resources/font/Pixeltype.ttf', 50)
	game_active = False
	start_time = 0
	update_player_score(0)
	bg_music = pygame.mixer.Sound('resources/audio/amongThieves.mp3')
	bg_music.play(loops = -1)

	# Sprites
	player = pygame.sprite.GroupSingle()
	player.add(myplayer.Player())
	power_up = pygame.sprite.GroupSingle()
	enemy_group = pygame.sprite.Group()

	# Timer 
	obstacle_timer = pygame.USEREVENT + 1
	power_up_timer = pygame.USEREVENT + 2
	pygame.time.set_timer(obstacle_timer, int(game_sprites.EnemySprite.Level.EASY))
	pygame.time.set_timer(power_up_timer, int(20000))
	game_sprites.EnemySprite.game_level = "EASY"


	while True:
		for event in pygame.event.get():	
			update_game_level()
			display_game_level()

			if player.sprite.player_lives == 0 and game_active:
				game_active = False
				isPersonalHighestScoreUpdated = update_score()
				if isPersonalHighestScoreUpdated:
					logger.debug("You have broken the record and having higest score of %s", score)
				
				
			if event.type == pygame.QUIT:
				pygame.quit()
				dbConnection.close() 
				exit()

			if game_active:
				if event.type == obstacle_timer:
					display_higest_score()
					enemyChoice = choice([ENEMY_TYPE_ALIEN, ENEMY_TYPE_SNAIL, ENEMY_TYPE_FLY, ENEMY_TYPE_SNAIL, ENEMY_TYPE_SNAIL, ENEMY_TYPE_NIGHTBORNE])
					logger.debug('Create Enemy of type %s', enemyChoice)
					enemy_group.add(game_sprites._get_Enemy_Sprite(enemyChoice))
				if event.type == power_up_timer:
					power_up.add(game_sprites.PowerUpSprite())
			
			else:
				if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
					game_active = True
					update_player_score(0)
					player.sprite.player_lives = 3
					isPersonalHighestScoreUpdated = update_score()
					display_higest_score()
					if isPersonalHighestScoreUpdated:
						logger.debug("You have broken the record and having higest score of %s", score)
					start_time = int(pygame.time.get_ticks() / 1000)


		if game_active:
			show_play_screen()
		else:
			if score == 0: 
				show_title_screen()
			else: 
				show_game_end_screen()

		pygame.display.update()
		clock.tick(60)
#------------------- Main program: End ----------------
		
if __name__ == "__main__":
	try:
		Main()
	except Exception as ex:
		logger.error('Game is terminated due to an error. Error: %s', ex)
		raise
