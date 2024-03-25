import pygame
import os
import sqlite3
import configparser
from sys import exit
from random import randint, choice

from sprites.constants import *
import sprites.game_sprites as game_sprites
import player.player as myplayer
import application_log
import constants

# Using configparser to read the properties files
config = configparser.ConfigParser()

# Read the resource property file to support different languages
config.read(constants.WORKING_DIR + constants.RESOURCE_PROPERTYFILE)

# added logger to have application logs in the log file.
logger = application_log.logger_config(__name__)

# This is the Main function for this application
def Main():
	WIDTH, HEIGHT = 800, 400
	clock = pygame.time.Clock()

	#------------------- Function: display_score ----------------
	# Displays the hightest score on the screen
	def display_higest_score():
		highestScoreRow = get_highest_score()
		hg_score_msg = config.get('Game', 'game.highest.score')
		hg_score_surf = game_font.render(hg_score_msg + f': {highestScoreRow}', False, 'RED')
		hg_score_rect = hg_score_surf.get_rect(center = (400,20))
		screen.blit(hg_score_surf, hg_score_rect)


	#------------------- Function: display_score ----------------
	# Displays the current score of the player
	def display_score():
		current_time = int(pygame.time.get_ticks() / 1000) - start_time
		player_score_msg = config.get('Player', 'player.score')
		score_surf = game_font.render(player_score_msg + ': ' + str(current_time), False, (64,64,64))
		score_rect = score_surf.get_rect(center = (400,50))
		screen.blit(score_surf,score_rect)
		return current_time


	#------------------- Function: display_lives ----------------
	# Displays the number of lives of the player
	def display_lives():
		lives_msg = config.get('Player', 'player.lives')
		lives_surf = game_font.render(lives_msg + ': ' + str(player.sprite.player_lives), False, (64,64,64))
		lives_rect = lives_surf.get_rect(center = (600,50))
		screen.blit(lives_surf, lives_rect)


	#------------------- Function: display_game_level ----------------
	# Displays the game's difficulty level
	def display_game_level():
		game_level_msg = config.get('Player', 'player.game.level')
		level_surf = game_font.render(game_level_msg + ': ' + game_sprites.EnemySprite.game_level, False, (64,64,64))
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
		logger.debug("database_init - going to create/open db connection...")
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
	
	#------------------- Function: get_all_players_ranking ----------------
	# Utility function to get player's score order by score
	def get_all_players_ranking():
		return cursor.execute("select * from higest_score order by score desc").fetchall()
	
	#------------------- Function: get_personal_highest_score ----------------
	# Utility function to get the player's personal highest score from the database
	def get_player_ranking():
		players = get_all_players_ranking()
		global rank
		rank = 0
		for idx, player in enumerate(players):
			if player[0] == player_name:
				return idx+1

		return rank


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
		player_stand = pygame.image.load(constants.PLAYER_SPRITE_STAND_IMG).convert_alpha()
		player_stand = pygame.transform.rotozoom(player_stand,0,2)
		player_stand_rect = player_stand.get_rect(center = (400,200))
		game_name = game_font.render(player_name + ' ' + config.get('Player', 'player.runner'), False, (111,196,169))
		game_name_rect = game_name.get_rect(center = (400,80))
		game_start_message = game_font.render(game_start_text, False, (111,196,169))
		game_start_rect = game_start_message.get_rect(center = (400,370))

		screen.fill((94,129,162))
		screen.blit(player_stand, player_stand_rect)
		screen.blit(game_name,game_name_rect)
		screen.blit(game_start_message,game_start_rect)
		
		pygame.draw.rect(screen, colour, input_rect, 2)
		input_surface = game_font.render(player_name, True, WHITE)
		screen.blit(input_surface, (input_rect.x + 5, input_rect.y + 5))

		pygame.display.flip()


	#------------------- Function: show_game_end_screen ----------------
	# shows the 'Game End Screen'
	def show_game_end_screen():
		screen.fill((94,129,162))

		# Player Name
		player_name_msg = game_font.render(player_name, False, (111,196,169))
		player_name_msg_rect = player_name_msg.get_rect(center = (400, 50))
		screen.blit(player_name_msg, player_name_msg_rect)
		
		# Current Score
		your_score_msg = config.get('Player', 'player.current.score')
		score_message = game_font.render(your_score_msg + ': ' + str(score), False, (111,196,169))
		score_message_rect = score_message.get_rect(center = (400, 100))
		screen.blit(score_message, score_message_rect)
		
		# Personal Highest Score
		your_score_msg = config.get('Player', 'player.personal.highest')
		score_message = game_font.render(your_score_msg + ': ' + str(get_personal_highest_score()[1]), False, (111,196,169))
		score_message_rect = score_message.get_rect(center = (400, 150))
		screen.blit(score_message, score_message_rect)

		# Overall Ranking
		your_score_msg = config.get('Player', 'player.ranking')
		score_message = game_font.render(your_score_msg + ': ' + str(get_player_ranking()), False, (111,196,169))
		score_message_rect = score_message.get_rect(center = (400, 200))
		screen.blit(score_message, score_message_rect)

		# Restart Message
		game_restart_msg = config.get('Game', 'game.restart.msg')
		restart_message = game_font.render(game_restart_msg, False, (111,196,169))
		restart_message_rect = restart_message.get_rect(center = (400,350))
		screen.blit(restart_message, restart_message_rect)

		global not_game_end_screen
		not_game_end_screen = True

	
	#------------------- Function: show_play_screen ----------------
	# shows the 'Play Screen'
	def show_play_screen():
		sky_surface = pygame.image.load(constants.BACKGROUND_SKY_IMAGE).convert()
		ground_surface = pygame.image.load(constants.BACKGROUND_GROUND_IMAGE).convert()
		
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


	#------------------- Function: show_ranking_screen ----------------
	# shows the 'Ranking Screen'
	def show_ranking_screen():
		screen.fill((94,129,162))
		exit_button.draw(screen)	

		# Plaer Sprite Image
		player_tropy = pygame.image.load(constants.PLAYER_SPRITE_STAND_IMG).convert_alpha()
		player_tropy = pygame.transform.rotozoom(player_tropy,0,2)
		player_tropy_rect = player_tropy.get_rect(center = (150,150))
		screen.blit(player_tropy, player_tropy_rect)

		# Plaer Trophy Image
		player_tropy = pygame.image.load(constants.TROPHY_IMG).convert_alpha()
		player_tropy = pygame.transform.rotozoom(player_tropy,0,2)
		player_tropy_rect = player_tropy.get_rect(center = (650,150))
		screen.blit(player_tropy, player_tropy_rect)


		# Rank
		players_ranking_msg = config.get('Player', 'players.ranking')
		player_message = game_font.render(players_ranking_msg, False, 'Orange')
		player_message_rect = player_message.get_rect(center = (400, 50))
		screen.blit(player_message, player_message_rect)


		players = get_all_players_ranking()
		for idx, player in enumerate(players):
			# show top 5 player's ranking
			if(idx < 5):
				player_rank = str(idx+1) + '.  ' + player[0] + ' (' + str(player[1]) + ')'
				player_message = game_font.render(player_rank, False, (111,196,169))
				player_message_rect = player_message.get_rect(center = (400, 50 + (50*(idx+1))))
				screen.blit(player_message, player_message_rect)

	
	#------------------- Function: update_player_score ----------------
	# Update the score
	def update_player_score(s):
		global score
		score = s


#-------------------------------------------------
#------------------- Main program ----------------
#-------------------------------------------------

	# Changing the current working directory
	os.chdir(constants.WORKING_DIR)

	global game_font
	global bg_music 
	global player_name
	global not_game_end_screen

	pygame.init()
	database_init()

	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	game_font = pygame.font.Font(constants.GAME_FONT, 50)
	bg_music = pygame.mixer.Sound(constants.BACKGROUND_MUSIC)
	bg_music.play(loops = -1)
	game_active = False
	not_game_end_screen = False
	start_time = 0
	update_player_score(0)
	player_name = ''
	input_rect = pygame.Rect(200, 300, 400, 30)
	colour = pygame.Color('black')
	player_ranking_screen = False

	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)

	game_start_text = config.get('Game', 'game.start.msg')
	pygame.display.set_caption(config.get('Game', 'game.caption'))
	
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

	# Button images
	replay_bttn_img = pygame.image.load(constants.BUTTON_REPLAY_IMG).convert_alpha()
	ranking_bttn_img = pygame.image.load(constants.BUTTON_RANKING_IMG).convert_alpha()
	quit_bttn_img = pygame.image.load(constants.BUTTON_QUIT_IMG).convert_alpha()
	exit_bttn_img = pygame.image.load(constants.BUTTON_EXIT_IMG).convert_alpha()
	# Button instances
	ranking_button = Button(200, 250, ranking_bttn_img, 1)
	replay_button = Button(380, 250, replay_bttn_img, 1)
	quit_button = Button(500, 250, quit_bttn_img, 1)
	exit_button = Button(350, 350, exit_bttn_img, 1)


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
				if event.type == pygame.KEYDOWN: 

					if event.key == pygame.K_BACKSPACE:						
						logger.debug('Player name BEFORE: ' + player_name)
						if len(player_name) > 0:
							game_start_text = config.get('Game', 'game.start.msg')
							player_name = player_name[:-1]
						logger.debug('Player name AFTER: ' + player_name)

					elif event.key == pygame.K_RETURN:
						logger.debug("Pressed Enter")
						# Validation: player name cannot be empty
						if len(player_name) == 0:
							game_start_text = config.get('Game', 'game.input.validation.msg')
						else:
							game_active = True
							update_player_score(0)
							player.sprite.player_lives = 3
							isPersonalHighestScoreUpdated = update_score()
							display_higest_score()
							if isPersonalHighestScoreUpdated:
								logger.debug("You have broken the record and having higest score of %s", score)
							start_time = int(pygame.time.get_ticks() / 1000)
					else:
						logger.debug('Player name BEFORE: ' + player_name)
						if len(player_name) < 23:
							player_name += event.unicode
							game_start_text = config.get('Game', 'game.start.msg')
						logger.debug('Player name AFTER: ' + player_name)


		if game_active:
			show_play_screen()

		elif player_ranking_screen:
			if(exit_button.draw(screen)):
				player_ranking_screen = False
			show_ranking_screen()

		else:
			if score == 0: 
				show_title_screen()
			else: 				
				show_game_end_screen()
	
				if(quit_button.draw(screen)):
					pygame.quit()
					dbConnection.close() 
					exit()

				elif(replay_button.draw(screen)):
					game_active = True
					update_player_score(0)
					player.sprite.player_lives = 3
					isPersonalHighestScoreUpdated = update_score()
					display_higest_score()
					if isPersonalHighestScoreUpdated:
						logger.debug("You have broken the record and having higest score of %s", score)
					start_time = int(pygame.time.get_ticks() / 1000)

				elif(ranking_button.draw(screen)):
					player_ranking_screen = True
					


		pygame.display.update()
		clock.tick(60)

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
		

if __name__ == "__main__":
	try:
		Main()
	# Catch the exception and add the error message in the application logfile
	except Exception as ex:
		logger.error('Game is terminated due to an error. Error: %s', ex)
		raise


