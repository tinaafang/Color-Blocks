import pygame
import random

def main():
    pass

if __name__ == '__main__':
    main()


# Define some colors
black = (0,0,0)
white = (255,255,255)
yellow = (255,210,2)

# Create lists for the enemy's direction choices, each list is consist of a large amount(75 or 100) of same number so that even in a randomly selecting method, the system will probably keep selecting the same direction to keep a continuous pathway. 
up = [i*0 for i in range(100)] # number 0 represets up
down = [i*0+1 for i in range(75)] # number 1 represets down
left = [i*0+2 for i in range(100)] # number 2 represets left
right = [i*0+3 for i in range(75)] # number 3 represets right
direction_choice = [up,down,left,right]
# [0,1,2,3] is also added to each of the direction list so that the enemy also have the chance to change direction. 
for i in direction_choice:
	for ii in range(4):
		i.append(ii)

# Initiate the colored block list and recolored block list
colored_block_list = []
recolored_block_list = []



# Class that manage all blocks
class ColorBlocks(pygame.sprite.Sprite):
	def __init__(self,color,pos_x,pos_y,width,height):
		super().__init__()
		# Color blocks are pygame surfaces with given width and height, rectangles are drawn to move the block surfaces
		self.image = pygame.Surface([width,height])
		self.rect = self.image.get_rect()
		# Set the location of the block surfaces
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.rect.topleft = (self.pos_x,self.pos_y)
		
	# Update the color of the block
	def update(self,color):
		self.image.fill(color)

	# Get the color of the block
	def get_color(self):
		if( self.image.get_at((0,0))[:3]) == (255,210,2):
			return("yellow")
		if self.image.get_at((0,0))[:3] == (255,255,255):
			return ("white")

	# Get the location of the block
	def get_position(self):
		return self.pos_x,self.pos_y
			
# Class that manage the speeding shoes
class Shoes(pygame.sprite.Sprite):
	def __init__(self,shoes,screen):
		# Load the shoes image and draw a rect around to move the shoes image
		self.image = pygame.image.load(shoes)
		self.rect = self.image.get_rect()
		self.screen = screen
		# Set the location of the shoes 
		self.rect.topleft=(520,90)
		
	# Generate random x and y values to hide the shoes
	def get_position(self):
		self.random_x = random.randrange(0,550)
		self.random_y = random.randrange(0,550)
		return self.random_x,self.random_y

	# Detect if the shoes is found
	def isFound(self,character_x,character_y):
		# random_x and random_y are the current localtion of the shoes, character_x and character_y are the current location of the main character. If their differences are less than 10, the shoes is considered found. 
		if abs(self.random_x-character_x) <10 and abs(self.random_y-character_y) <10:
			return True

	# Blit the shoes to the screen for 15 seconds
	def draw(self):
		# main_character.current represents the time since the game start, main_character.shoes_found represents the time when the shoes is found, if the difference between these two are less than 15 seconds, the shoes image is blited on the screen. (main_character.shoes_found is initial at 0, so the image will not be blited when it is 0 )
		if main_character.current - main_character.shoes_found < 15000 and main_character.shoes_found != 0:
			self.screen.blit(self.image, self.rect)


# The class that manage the main character
class Character(pygame.sprite.Sprite):
	def __init__(self,picture,pos_x,pos_y,screen,lives):
		super().__init__()
		# Load the image of the main character and draw a rectangle around to move it. 
		self.image = pygame.image.load(picture)
		self.rect = self.image.get_rect()
		self.screen = screen
		# pos_x and pos_y are the initial location of the character
		self.pos_x = pos_x
		self.pos_y = pos_y
		# current is the time since the pygame initialtes
		self.current = int(pygame.time.get_ticks())
		# lives, collide times, message and shoes found are initialed
		self.lives = lives
		self.collide_times = [0]
		self.message = ""
		self.shoes_found = 0
		
	# The character's lives will be deducted and a message is print when losing lives
	def losing_lives(self):
		# self.collide_times is a list that collectes the time values when the character intersects the enemy
		self.collide_times.append(self.collide_time)
		# When the character intersects the enemy, it will not lose another life in the next three seconds
		# self.collide_times[-1] and self.collide_times[-2] are the lastest two times that the character collides with the enemy, if the difference of these two time values is less than 3 seconds, the lastest time value will be removed from the list, so the lives do not decrease
		if self.collide_times[-1] - self.collide_times[-2] < 3000:
				self.collide_times.remove(self.collide_times[-1])
		# Otherwise, prepare the on screen message that says "lives -1" and mark the time when the lives is deducted(game_state.starting_time represents the time that the pygame is initialted but the game is not start yet. ) 
		else:
			self.losing_lives_time = int(pygame.time.get_ticks())
			self.losing_lives_time -= game_state.starting_time
			self.message = "lives -1"
		# Actual deduction the lives
		self.lives = 3 - (len(self.collide_times)-1)
		
	# Prepare and print different game over messages on screen
	def game_over_message(self,game_completed):
		# Assign different strings to the message varaible according to the performance of the character
		if game_completed:
			message = "Congratulations! Game completed."
		if not game_completed:
			if self.current >= 60000:
				message = "Time's up"
			elif self.lives < 1:
				message = "You are dead"
			
		# Render and blit the game over message
		game_over_message = font.render(message,True, black)
		self.screen.blit(game_over_message,(300-game_over_message.get_width()/2,225) )
	
	
	# Get the current location of the character
	def get_position(self):
		return self.pos_x,self.pos_y

	# Assign new location to the character
	def set_position(self,x,y):
		self.pos_x = x
		self.pos_y = y
		self.rect.topleft=(self.pos_x,self.pos_y)

	# Blit the image of the character
	def draw(self):
		self.screen.blit(self.image, self.rect)

	# Move the character upwords
	def up(self): 
		# The moving speed is 6 within 15 seconds when the character collides with the enemy
		# self.current represents the time since the game start, self.shoes_found represents the time since the shoes is found, when the difference between these two are lessen than 15 seconds and the time of shoes found is not equal to its initial value 0(otherwise the character will move at speed 6 during the first 15 seconds of the game), the charactrer will move in doubled speed 6
		if self.current - self.shoes_found < 15000 and self.shoes_found != 0:
			self.pos_y -= 10
		
		# The character normally move in speed 3
		else:
			self.pos_y -= 5
		# The character cannot move forward when reaching the screen border
		if self.pos_y <0:
			self.pos_y = 0
		# Move the character to the new location and set the image for moving upward
		self.rect.topleft=(self.pos_x,self.pos_y)
		self.image = pygame.image.load("images/up.png")
	
	# Using similar method in self.up() to move the character downwards
	def down(self):
		if int(self.current) - self.shoes_found < 15000 and self.shoes_found != 0:
			self.pos_y += 10
			
		else:
			self.pos_y += 5

		
		if self.pos_y> 550:
			self.pos_y = 550

		self.rect.topleft=(self.pos_x,self.pos_y)
		self.image = pygame.image.load("images/down.png")
	# Using similar method in self.up() to move the character to the left
	def left(self):
		if self.current - self.shoes_found < 15000 and self.shoes_found != 0:
			self.pos_x -= 10
		
		else:
			self.pos_x -= 5

		if self.pos_x <0:
			self.pos_x = 0
	
		self.rect.topleft=(self.pos_x,self.pos_y)
		self.image = pygame.image.load("images/left.png")
	# Using similar method in self.up() to move the character to the right
	def right(self):
		if int(self.current) - self.shoes_found < 15000 and self.shoes_found != 0:
			self.pos_x += 10
			
		else:
			self.pos_x += 5
		if self.pos_x>550:
			self.pos_x = 550
			
		self.rect.topleft=(self.pos_x,self.pos_y)
		self.image = pygame.image.load("images/right.png")

# Class that manage the enemy
class Enemy(pygame.sprite.Sprite):
	def __init__(self,picture,pos_x,pos_y,screen):
		super().__init__()
		# Load the image of the enemy and draw a rectangle around to move it
		self.image = pygame.image.load(picture)
		self.rect = self.image.get_rect()
		# Initiate the location of the enemy and move it to the initial location
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.screen = screen
		self.rect.topleft = (self.pos_x,self.pos_y)
		# Initialize the direction, 0,1,2,3 for up,down,left,right
		self.direction = random.choice([0,1,2,3])
	
	# Blit the enemy to the screen
	def draw(self):
		self.screen.blit(self.image,self.rect)
	
	# Move the enemy to the new location
	def set_position(self,x,y):
		self.pos_x = x
		self.pos_y = y
		self.rect.topleft=(self.pos_x,self.pos_y)

	# Make the enemy moves randomly
	def move(self,up,down,left,right):
		# self.direction is a randomly chosen value in the __init__ function
		if self.direction == 0:
			# If the enemy reaches the screen border, it would go in a opposite direction
			if self.pos_y <0:
				self.direction = 1
				self.pos_y = 0
			
			# Otherwise the enemy moves mostly upwards(since the value in the list "up" is mostly 0)
			else:
				self.direction = random.choice(up)
			self.pos_y -= 5
			self.image = pygame.image.load("images/e_up.png")
			
		# Similar method is used for direction down
		elif self.direction == 1:
			if self.pos_y> 550:
				self.direction = 0
				self.pos_y = 550
				
			else:
				self.direction = random.choice(down)
			self.pos_y += 5
			self.image = pygame.image.load("images/e_down.png")
			
			
		# Similar method is used for direction down
		elif self.direction == 2:
		#def left(self):
			if self.pos_x <0:
				self.direction = 3
				self.pos_x = 0
				
			for i in range(100):
				
				self.direction = random.choice(left)
			self.pos_x -= 5
			self.image = pygame.image.load("images/e_left.png")
			
		# Similar method is used for direction down
		elif self.direction == 3:
		#def right(self):
			if self.pos_x>550:
				self.direction = 2
				self.pos_x = 550
				
			for i in range(75):
				self.direction = random.choice(right)
			self.pos_x += 5
			self.image = pygame.image.load("images/e_right.png")

		# Lastly, move the enemy to the new location
		self.rect.topleft=(self.pos_x,self.pos_y)

# Class that manage buttons
class Button(pygame.sprite.Sprite):
	def __init__(self,pos_x,pos_y,width,height,color,outline_color,border,text,screen,pos,space):
		super().__init__()
		# Initialize the location, with, height, color, border with, in box text, font, border color, spaces that is needed to put the in box texts right in the middle of the button, and lastly the position of the mouse
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.width = width
		self.height = height
		self.color = color
		self.border = border
		self.screen = screen
		self.text = text
		self.font = font
		self.outline_color = outline_color
		self.space = space

	# Draw the button and blit the text
	def draw(self):
		# Draw two rectangles, one for the button itself, one for the border
		pygame.draw.rect(self.screen,self.color,[self.pos_x,self.pos_y,self.width,self.height])
		pygame.draw.rect(self.screen,self.outline_color,[self.pos_x,self.pos_y,self.width,self.height],self.border)

	  # Blit the texts to the screen
		button_text = self.font.render(self.text,True, black)
		self.screen.blit(button_text,[self.pos_x+self.space,self.pos_y+(button_text.get_height()/2)])


	# Detect if the mouse is over the button
	def isOver(self,pos):
		# self.pos[0] or self.pos[1] represents current locati0n of the mouse, self.pos_x(+self.width) and self.pos_y(+self.height) represent the area of the button, when the mouse is over the area of the button, the function returns True
		if pos[0]>self.pos_x and pos[0]<self.pos_x+self.width:
			if pos[1]>self.pos_y and pos[1]<self.pos_y+self.height:
				return True

# Class that manage the state of the entire game
class GameState():
	def __init__(self):
		# Initialize the state to the intro page
		self.state = "intro"
		# Initialize the starting time, which is the time  when a game starts
		self.starting_time = 0
		self.done = False
		
	# Manage the state of the game, call different method acccording to different game state
	def state_manager(self):
		if self.state == "intro":
			self.intro()
		if self.state == "main game":
			level_two = False
			self.main_game(level_two)
		if self.state == "level two":
			self.level_two()
		if self.state == "main game: level two":
			level_two = True
			self.main_game(level_two)
		if self.state == "game over":
			game_completed = False
			self.game_over(game_completed)
		if self.state == "set up":
			level_two = False
			self.set_up(level_two)
		if self.state == "set up: level two":
			level_two = True
			self.set_up(level_two)
		if self.state == "instruction":
			self.instruction()
		if self.state == "game completed":
			game_completed = True
			self.game_over(game_completed)

	# Set up the game when a game starts
	def set_up(self,level_two):
		# Move the character to the top left corner
		main_character.set_position(0,0)
		# Initialize the character's lives at 3
		main_character.lives = 3
		# Initialize the list that collects the time when character collides with the enemy
		main_character.collide_times = [0]
		# Initialize the following time values to 0
		main_character.shoes_found = 0
		main_character.losing_lives_time = 0
		# Initialize the character image
		main_character.image = pygame.image.load("images/right.png")
		# Move the enemy to the bottom right corner and load the iamge of the enemy
		enemy1.set_position(550,550)
		enemy1.image = pygame.image.load("images/e_left.png")
		enemy2.set_position(550,0)
		enemy2.image = pygame.image.load("images/e_down.png")
		# If the game is in level two, move the second enemy to the up right corner and load the image for it
		if level_two:
			enemy3.set_position(0,550)
			enemy3.image = pygame.image.load("images/e_right.png")
		# Hide the shoes to a random place
		shoes.random_x,shoes.random_y = shoes.get_position()
		# Clear the colored and the uncolored block lists
		colored_block_list.clear()
		recolored_block_list.clear()
		# Draw all blocks and color them in yellow
		block_group.draw(screen)
		block_group.update(yellow)
		# Draw the character and the enemy
		main_character.draw()
		enemy1.draw()
		enemy2.draw()
		# If the game is at level 2, set the game state to "main game: level two" that calls the level two version of the main game
		if level_two:
			self.state = "main game: level two"
		# Otherwise, just set the stage that calls the normal version of the game
		else:
			self.state = "main game"
		
	
	# The intro page fo the game
	def intro(self):
		
		for event in pygame.event.get():
			# Quit the game if the the player chooses to
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type == pygame.MOUSEBUTTONUP:
					if start_button.isOver(pos) == True:
						# If the mouse is clicked on the area of the start button, starting time is recorded and the game will be set up
						self.starting_time = int(pygame.time.get_ticks())
						self.state = "set up"
					if instruction_button.isOver(pos) == True:
						# If the mouse is clicked on the area of the instruction button, the instruction page is initialize to 1 and the players will be directed to the instruction page
						self.instruction_page = 1
						self.state = "instruction"
		
		# Blit the background
		screen.fill(white)
		screen.blit(background,(0,0))
		# Render the title texts and the texts that creats shadow effect, and blit both on teh screen
		title = header.render("Color Blocks",True,black)
		title_shadow = header.render("Color Blocks",True,white)
		screen.blit(title_shadow,(303-title.get_width()/2,183))
		screen.blit(title,(300-title.get_width()/2,180))
		# Draw both instruction button and the start button
		instruction_button.draw()
		start_button.draw()
		# Update the screen
		#pygame.display.flip()

	# The instruction page
	def instruction(self):
		# Initialize the instruction variable
		instruction = background
		for event in pygame.event.get():
			# Quit the game if the player chooses to
			if event.type == pygame.QUIT:
				self.done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# If the mouse clicks on the return button, return to the intro page
				if return_button.isOver(pos) == True:
					self.state = "intro"
				# If the mouse clicks on the next button, the instruction page is incremented
				if next_button.isOver(pos)==True:
					self.instruction_page += 1

		# Set the screen background
		screen.fill(white)
		# Stores the instruction pages to the instruction varaible
		if self.instruction_page == 1:
			instruction = pygame.image.load("images/instruction-1.jpg")
		if self.instruction_page == 2:
			instruction = pygame.image.load("images/instruction-2.jpg")
		if self.instruction_page == 3:
			instruction = pygame.image.load("images/instruction-3.jpg")
		if self.instruction_page == 4:
			instruction = pygame.image.load("images/instruction-4.jpg")
		if self.instruction_page == 5:
			instruction = pygame.image.load("images/instruction-5.jpg")
		# If the page number is 6, back to the intro page
		if self.instruction_page >= 6:
			self.state = "intro"

		# Blit the instruction page to the screen
		screen.blit(instruction,(0,0))
		# Blit the two buttons
		return_button.draw()
		next_button.draw()
		# Update the screen
		#pygame.display.flip()
		
	# The main game 
	def main_game(self,level_two):
		# Initialize the messge variable for on screen message
		message = ""
		# Set up the time since the game starts, which equals the time that pygame is initiated minus the time that the game starts
		main_character.current = int(pygame.time.get_ticks())
		main_character.current -= int(self.starting_time)
	
		# Stores the current location of the main_character to the variables chracter_x and character_y
		character_x,character_y = main_character.get_position()


		# ----- Shoes Found ------
		# Record the time when the shoes is found
		if shoes.isFound(character_x,character_y) == True:
			main_character.shoes_found = int(pygame.time.get_ticks())
			main_character.shoes_found -= int(self.starting_time)
		# On screen message is set to "Speeding up" for two seocnds once the shoes is found
		if main_character.current - main_character.shoes_found <2000 and main_character.shoes_found != 0:
			message = "Speeding up"


		for event in pygame.event.get():
			# Quit the game if the player chooses to
			if event.type == pygame.QUIT:
				self.done = True

			elif event.type == pygame.KEYDOWN:
				# The enemy mvoes when the character is moving
				enemy1.move(up,down,left,right)
				enemy2.move(up,down,left,right)
				# If the game is at level 2, the second enemy moves as well
				if level_two:
					enemy3.move(up,down,left,right)
				# If the keys are pressed, multiple key_down event will be generated, instead of just one event
				pygame.key.set_repeat(10,50)
				# If the arrow key is pressed, the characer moves in teh corresponding direction
				if event.key == pygame.K_LEFT:
					main_character.left()
					
				if event.key == pygame.K_RIGHT:
					main_character.right()
					
				if event.key == pygame.K_UP:
					main_character.up()
					
				if event.key == pygame.K_DOWN:
					main_character.down()
	
		# ------ Coloring ------
		# Store all blocks that the character passes by
		colored_block = pygame.sprite.spritecollide(main_character,block_group,False)

		# Append the blocks into colored block list
		for i in colored_block:
			if i not in colored_block_list:
				colored_block_list.append(i)
		
		# For all blocks that the character passes by, color them in white
		for i in colored_block_list:
			if i.get_color() == "yellow":
				i.update(white)
			
		# Use similar method for the enemies, first store the blocks that the enemy(and the second enemy if it is a level two game) passes by
		recolored_block_one = pygame.sprite.spritecollide(enemy1,block_group,False)
		recolored_block_two = pygame.sprite.spritecollide(enemy2,block_group,False)
		recolored_block_three = pygame.sprite.spritecollide(enemy3,block_group,False)

		if level_two:
			for i in recolored_block_three:
				recolored_block_one.append(i)
		# For all blocks that the enemy passes by, remove them from the colored block list so that they return to color yellow
		for i in recolored_block_one:
			if i in colored_block_list:
				colored_block_list.remove(i)
		for i in recolored_block_two:
			if i in colored_block_list:
				colored_block_list.remove(i)
		
		# ------ Losing Lives ------
		# For a normal level 1 game
		if not level_two:
			# If the character collides with the enemy, record the time of collision and call main_character.losing_lives()
			if pygame.sprite.collide_rect(main_character,enemy1) or pygame.sprite.collide_rect(main_character,enemy2):
				main_character.collide_time = int(pygame.time.get_ticks())
				main_character.collide_time -= int(self.starting_time)
				main_character.losing_lives()
			# If the difference between the current time and the time of collision recorded above is lessen than 2 seconds, the on screen message becomes "lives-1" which is set up already calling the main_character.losing_lives() method
			if main_character.current - main_character.losing_lives_time <2000 and main_character.losing_lives_time != 0:
				message = main_character.message
			
		# There is no much different for the level 2 game, except it also check the collision of the character and the second enemy
		if level_two:
			if pygame.sprite.collide_rect(main_character,enemy1) or pygame.sprite.collide_rect(main_character,enemy2) or pygame.sprite.collide_rect(main_character,enemy3):
				main_character.collide_time = int(pygame.time.get_ticks())
				main_character.collide_time -= int(self.starting_time)
				main_character.losing_lives()
			if main_character.current - main_character.losing_lives_time <2000 and main_character.losing_lives_time != 0:
				message = main_character.message
		

		# ------ On Screen Scores ------
		# The score formula: number of the colored blocks divided by the total number of blocks, then times 100 to get the percentage
		total_count = len(block_group)
		colored_count = len(colored_block_list)
		score = round(100*round(colored_count / total_count,4))
		# Render the score, the lives and the remaining time, which is just 60 seconds minus the current time
		printed_score = font.render("score: " +str(score),True, black)
		printed_lives = font.render("lives: "+str(main_character.lives),True,black)
		remaining_time = 30 - round(main_character.current/1000,0)
		printed_time = font.render("time:"+str(remaining_time),True,black)
		
		# Record the time when the score reaches 30
		score30_time = 0
		if score == 30:
			score30_time = int(pygame.time.get_ticks())
			score30_time -= self.starting_time
		# Generate a message that says "Score 30!" that lasts for two seconds 
		if main_character.current - score30_time < 2000 and score30_time != 0:
			message = "Score 30!"


		# ----- Game Over -----
		# Game over when there is 0 lives
		if main_character.lives == 0:
			self.state = 'game over'
	
		# When current time reaches 30 secodns, if score < 30, game over; if score >= 30, the game either comes to the next level or the game is completed. 
		if main_character.current >= 30000:
			if level_two:
				if score < 30:
					self.state = "game over"
				if score >= 30:
					self.state = "game completed"
			else:
				if score < 30:
					self.state = "game over"
				elif score >=30:
					self.state = "level two"
			
			
			
		# Set the background
		screen.fill(white)
		# Draw the blocks and color them in yellow
		block_group.draw(screen)
		block_group.update(yellow)
		# Draw the character and the enemy, as well as the second enemy if it is a level 2 game
		main_character.draw()
		enemy1.draw()
		enemy2.draw()
		if level_two:
			enemy3.draw()
		# Draw the shoes 
		shoes.draw()
		# Blit the on screen score, lives and time
		screen.blit(printed_lives, [450,20])
		screen.blit(printed_score, [450,45])
		screen.blit(printed_time, [450,70])
		# Blit the on screen message
		on_screen_message = font.render(message,True, black)
		screen.blit(on_screen_message,(300-on_screen_message.get_width()/2,225) )
		# Update the screen
		#pygame.display.flip()


	# When the game is over
	def game_over(self,game_completed):
		# Get the posistion of the mouse for start again button
		start_again_button.pos = pygame.mouse.get_pos()
		
		for event in pygame.event.get():
			# Quit the game if the player clicks on the QUit
				if event.type == pygame.QUIT:
					self.done = True
				elif event.type == pygame.MOUSEBUTTONDOWN:
						if start_again_button.isOver(pos) == True:
							# If the mouse click on the start again button, the player will be starting another game, the starting time is renewed as the game starts 
							self.starting_time = int(pygame.time.get_ticks())
							self.state = "set up"
						if home_button.isOver(pos) == True:
							# If the mouse click on the start again button, the player will be starting another game, the starting time is renewed as the game starts 
							self.state = "intro"
		# Set the background
		screen.fill(white)
		screen.blit(background,(0,0))
		# Draw the start again button
		start_again_button.draw()
		home_button.draw()
		# Blit the game over messages that tells why the game is ended
		main_character.game_over_message(game_completed)
		# Update the screen
		#pygame.display.flip()

	# If the player enter level 2 of the game
	def level_two(self):
		for event in pygame.event.get():
			# Quit the game if the player clicks to quit
				if event.type == pygame.QUIT:
					self.done = True
				elif event.type == pygame.MOUSEBUTTONUP:
						# If the player clicks on the level two button, set up a level two game and renew the starting time as the game starts
						if level_two_button.isOver(pos) == True:
							
							self.starting_time = int(pygame.time.get_ticks())
							self.state = "set up: level two"
						if home_button.isOver(pos) == True:
							self.state = "intro"
		
		# Set the background
		screen.fill(white)
		screen.blit(background,(0,0))
		# Draw the level two button
		level_two_button.draw()
		home_button.draw()
		# Update the screen
		#pygame.display.flip()

	 

# Initiate pygame and the mixer for the soud effect
pygame.init()
pygame.mixer.init()
# Store the background music
bgm = pygame.mixer.Sound("bgm.wav")

#pygame.key.set_repeat()
# set the height and width of the screen
screen_width = 600
screen_height = 600
size = [screen_width,screen_height]
# Set up the screen and the caption
screen = pygame.display.set_mode(size)
pygame.display.set_caption("COLOR BLOCKS")
# Get the position of the mouse
pos = pygame.mouse.get_pos()
# Set up different fonts
font = pygame.font.SysFont("Luxurious Roman" , 36, True, False)
header = pygame.font.SysFont("Luxurious Roman" ,90, True, False)
# Set up the background image
background = pygame.image.load("images/BG.png")
# Set up the colored blocklist and the recolored block list
colored_block_list = []
recolored_block_list = []
# manage how fast the screen update
clock = pygame.time.Clock()

# ------- Create Objects ------
# Game State
game_state = GameState()

# Color blocks group
block_group = pygame.sprite.Group()
# Create blocks that fill the entire screen, the size of the blocks is 5*5 pixels, add each blocks to the block group
block_width = 5
for i in range(int(screen_width/block_width)):
	for ii in range(int(screen_height/block_width)):
		block = ColorBlocks(black,i*block_width,ii*block_width,block_width,block_width)
		block_group.add(block)

# Shoes
shoes = Shoes("images/shoes.png",screen)

# Character 
main_character = Character("images/right.png",0,0,screen,3)

# Enemy
enemy1 = Enemy("images/e_left.png",screen_width-50,screen_height-50,screen)

enemy2 = Enemy("images/e_down.png",screen_width-50,0,screen)

enemy3 = Enemy("images/e_right.png",0,screen_height-50,screen)


# Buttons
# For intro page
instruction_button = Button(300,400,200,50,white,black,5,"How to Play",screen,pos,20)
start_button = Button(300,320,200,50,white,black,5,"Start",screen,pos,65)

# For instruction page
return_button = Button(350,500,200,50,white,black,5,"Return",screen,pos,60)
next_button = Button(100,500,200,50,white,black,5,"Next Page",screen,pos,30)

# For game over page
start_again_button = Button(200,300,200,50,white,black,5,"Play Again",screen,pos,30)
home_button = Button(200,380,200,50,white,black,5,"Home",screen,pos,60)

# To start level two
level_two_button = Button(200,300,200,50,white,black,5,"Level Two",screen,pos,30)

 

# -----------Main Program Loop---------------
while not game_state.done:
	# Loop the background music so it would not stop
	bgm.play(-1)
	# Get the position of the mouse
	pos = pygame.mouse.get_pos()
	# Play the game
	game_state.state_manager()
	# Limit to 60 frames per second
	clock.tick(60)
	# Update the screen
	pygame.display.flip()
	
			
			
pygame.quit()

