import pygame
import os
import sqlite3
from sys import exit
from random import randint, choice

# importing own classes
from player import Player
from obstacle import Obstacle

def Main():
	WIDTH, HEIGHT = 800, 400
	clock = pygame.time.Clock()

	#----------------------- Function display_score: Start ----------------
	# Displays the hightest score on the screen
	def display_higest_score():
		highestScoreRow = get_highest_score()
		hg_score_surf = test_font.render(f'Higest Score: {highestScoreRow}',False,'RED')
		hg_score_rect = hg_score_surf.get_rect(center = (400,20))
		screen.blit(hg_score_surf, hg_score_rect)
	#----------------------- Function collision_sprite: End ----------------

	#----------------------- Function display_score: Start ----------------
	# Displays the current score of the player
	def display_score():
		current_time = int(pygame.time.get_ticks() / 1000) - start_time
		score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
		score_rect = score_surf.get_rect(center = (400,50))
		screen.blit(score_surf,score_rect)
		return current_time
	#----------------------- Function collision_sprite: End ----------------

	#----------------------- Function display_lives: Start ----------------
	# Displays the number of lives of the player
	def display_lives():
		lives_surf = test_font.render(f'Lives: {player.sprite.player_lives}',False,(64,64,64))
		lives_rect = lives_surf.get_rect(center = (600,50))
		screen.blit(lives_surf, lives_rect)
	#----------------------- Function display_lives: End ----------------

	#----------------------- Function display_game_level: Start ----------------
	# Displays the game's difficulty level
	def display_game_level():
		level_surf = test_font.render(f'Level: {Obstacle.game_level}',False,(64,64,64))
		level_rect = level_surf.get_rect(center = (200,50))
		screen.blit(level_surf, level_rect)
	#----------------------- Function display_game_level: End ----------------

	#----------------------- Function collision_sprite: Start ----------------
	# Checks if sprite collides with enemy and return true/false
	def collision_sprite():
		if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
			obstacle_group.empty()
			player.sprite.player_lives -= 1
			player.sprite.image = player.sprite.player_dead
			game_active = False
			print("player lives = ", player.sprite.player_lives)
	#----------------------- Function collision_sprite: End ----------------

	#----------------------- Function database_init: Start ----------------
	# Initialise the database tables, connection, etc
	def database_init():
		print("database_init - going to create/open db connection.....1")
		global dbConnection, cursor, highestScoreRow
		dbConnection = sqlite3.connect("database/pygameRun.db") # opening the database connection
		cursor = dbConnection.cursor()
		cursor.execute("create table if not exists higest_score(name text, score integer)")
		highestScoreRow = get_highest_score()
		print("database_init - created/opened db connection with higest_score table having value = ", highestScoreRow)
	#----------------------- Function database_init: End ----------------

	#----------------------- Function get_personal_highest_score: Start ----------------
	# Utility function to get the player's personal highest score from the database
	def get_personal_highest_score():
		return cursor.execute("select * from higest_score where name = ?", (player_name,)).fetchone()
	#----------------------- Function get_personal_highest_score: End ----------------

	#----------------------- Function get_highest_score: Start ----------------
	# Utility function to get the higest score from the database
	def get_highest_score():
		return cursor.execute("select * from higest_score where score = (select max(score) from higest_score)").fetchone()
	#----------------------- Function get_highest_score: End ----------------

	#----------------------- Function update_score: Start ----------------
	# Insert or Update the score of current player in the database
	def update_score():
		retValue = False
		print("update_score - **score = ", score)
		personalhighestScoreRow = get_personal_highest_score()
		if personalhighestScoreRow == None:
			print("*************** INSERT")
			cursor.execute("insert into higest_score(name, score) values(?,?)", (player_name, score))
			cursor.connection.commit()
		elif (isinstance(personalhighestScoreRow[1], (int)) and personalhighestScoreRow[1] < score):
			print("*************** UPDATE")
			cursor.execute("update higest_score set score = ? where name is ?", (score, player_name))
			cursor.connection.commit()
			retValue = True
		print(cursor.execute("select * from higest_score").fetchall())
		return retValue
	#----------------------- Function update_score: End ----------------

	#----------------------- Function update_game_level: Start ----------------
	# updates the game's difficulty level
	def update_game_level():
		if score > 30:
			pygame.time.set_timer(obstacle_timer, int(Obstacle.Level.HARDEST))
			Obstacle.game_level = Obstacle.Level.HARDEST.name
		elif score > 20:
			pygame.time.set_timer(obstacle_timer, int(Obstacle.Level.HARD))
			Obstacle.game_level = Obstacle.Level.HARD.name
		elif score > 10:
			pygame.time.set_timer(obstacle_timer, int(Obstacle.Level.MEDIUM))
			Obstacle.game_level = Obstacle.Level.MEDIUM.name
		else:
			pygame.time.set_timer(obstacle_timer, int(Obstacle.Level.EASY))
			Obstacle.game_level = Obstacle.Level.EASY.name
	#----------------------- Function update_game_level: End ----------------


#----------------------- Main program: Start ----------------

	
	# Changing the current working directory
	os.chdir('C:/GitHub/PygameRun') #NOTE: Change this path as per your project location
	player_name = input("Enter your name: ")
	database_init()
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption(player_name + ' - run run and win!')
	clock = pygame.time.Clock()
	test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
	game_active = False
	start_time = 0
	score = 0
	global bg_music 
	bg_music = pygame.mixer.Sound('audio/amongThieves.mp3')
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

	game_name = test_font.render(player_name + ' Runner',False,(111,196,169))
	game_name_rect = game_name.get_rect(center = (400,80))

	game_message = test_font.render('Hey, Press space to run',False,(111,196,169))
	game_message_rect = game_message.get_rect(center = (400,330))

	# Timer 
	obstacle_timer = pygame.USEREVENT + 1
	pygame.time.set_timer(obstacle_timer, int(Obstacle.Level.EASY))
	Obstacle.game_level = "EASY"


	while True:
		for event in pygame.event.get():	
			update_game_level()
			display_game_level()

			if player.sprite.player_lives == 0 and game_active:
				game_active = False
				isPersonalHighestScoreUpdated = update_score()
				if isPersonalHighestScoreUpdated:
					print("You have broken the record and having higest score of ", score)
				
				
			if event.type == pygame.QUIT:
				pygame.quit()
				dbConnection.close() 
				exit()

			if game_active:
				if event.type == obstacle_timer:
					display_higest_score()
					obstacle_group.add(Obstacle(choice(['snail','fly','snail','snail','Nightborne'])))
			
			else:
				if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
					game_active = True
					score = 0
					player.sprite.player_lives = 3
					isPersonalHighestScoreUpdated = update_score()
					display_higest_score()
					if isPersonalHighestScoreUpdated:
						print("You have broken the record and having higest score of ", score)
					start_time = int(pygame.time.get_ticks() / 1000)


		if game_active:
			screen.blit(sky_surface,(0,0))
			screen.blit(ground_surface,(0,300))
			display_higest_score()
			display_lives()
			display_game_level()
			score = display_score()
			
			player.draw(screen)
			player.update()

			obstacle_group.draw(screen)
			obstacle_group.update()

			collision_sprite()
		else:
			screen.fill((94,129,162))
			screen.blit(player_stand,player_stand_rect)

			score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
			score_message_rect = score_message.get_rect(center = (400,330))
			screen.blit(game_name,game_name_rect)
			restart_message = test_font.render(f'Press space to restart a new game',False,(111,196,169))
			restart_message_rect = restart_message.get_rect(center = (400,380))

			if score == 0: 
				screen.blit(game_message,game_message_rect)
			else: 
				screen.blit(score_message, score_message_rect)
				screen.blit(restart_message, restart_message_rect)

		pygame.display.update()
		clock.tick(60)
#----------------------- Main program: End ----------------
		
if __name__ == "__main__":
    Main()
