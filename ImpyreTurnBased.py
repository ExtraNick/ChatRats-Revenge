import pygame
import random
from pygame.sprite import Group

pygame.init()

clock = pygame.time.Clock()
fps = 60


#game window properties
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
pygame_icon = pygame.image.load('img/icon/ratge.ico')
pygame.display.set_icon(pygame_icon)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ChatRat's Revenge")

#define game variables
current_fighter = 1
total_fighters = 3
Boss_turn = 0
Boss_counter = 0
rat_turn = 0
rat_counter = 0
action_cooldown = 0
action_wait_time=90
boss_wait_time = 170
intro_cooldown = 0
intro_wait_time=156
special_counter_timer = 0
special_wait_time = 0
boss_attack = False
boss_clicked = False
attack = False
potion = False
boss_target = None 
potion_effect = 15
clicked = False
game_over = 0
Lucynamelist = ['Peggy Pyre', 'Padded Pyre', 'Flat Brat', 'Tiny', 'Sally Pyre', 'Pissy Pyre', 'Stinky Pyre', 'Juicy Lucy', 
'Titsie Pyre', 'Blue M&M', 'Cummander Pyre', 'White-haired Numi', 'Lucy PooPoo', 'Delululucy', 'Legussy Pyre']
randname = random.choice(Lucynamelist)
frameset = 0 #for resetting special's frame

#define fonts 
font = pygame.font.SysFont('Times New Roman', 26)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = ( 0, 0, 0)

#load images
#background image
background_img = pygame.image.load('img/Background/Preview/BackgroundPyreCroppedDark.png').convert_alpha()
#background ground image
ground_img = pygame.image.load('img/Background/Preview/BackgroundGround4.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/icon/panelImpyreRibbon.png').convert_alpha()
#potion image
potion_img = pygame.image.load('img/icon/SippieIcon.png').convert_alpha()
restart_img = pygame.image.load('img/icon/restartbutton2.png').convert_alpha()
restart_img = pygame.transform.scale(restart_img, (restart_img.get_width() * 3, restart_img.get_height() * 3))

#load victory and defeat images
victory_img = pygame.image.load('img/icon/hugew.png').convert_alpha()
defeat_img = pygame.image.load('img/icon/holdL.png').convert_alpha()
defeat_img = pygame.transform.scale(defeat_img, (defeat_img.get_width() * 2, defeat_img.get_height() * 2))
#mouse image
sword_img = pygame.image.load('img/icon/hammer.png').convert_alpha()
sword_img = pygame.transform.scale(sword_img, (sword_img.get_width() * 0.3, sword_img.get_height() * 0.3))
#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#Function for drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))
	screen.blit(ground_img, (0, 360))

#Function for drawing panel
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, (screen_height-bottom_panel) - 20))
	#show player stats
	draw_text(f'{ratJAM1.name}', font, white, 100, screen_height - bottom_panel + 30)
	draw_text(f'HP: {ratJAM1.hp}', font, white, 275, screen_height - bottom_panel + 30)
	for count, i in enumerate(wiggly_list):
		#show name and health of wigglie
		draw_text(f'{i.name} HP: {i.hp}', font, white, 440 + (count * 185), (screen_height - bottom_panel +30))
#----------------------------------------------------BUTTON--------------------------------------------------
#button class
class Button():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
#--------------------------------------------------------------------------------------------------------------

class ratJAM:
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.hp = max_hp
		self.max_hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0 #0 - idle, 1 - attack, 2 - hurt, 3 - deadge, 4 - victory
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(28):
			img = pygame.image.load(f'img/{self.name}/idle/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(14):
			img = pygame.image.load(f'img/{self.name}/attack/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load hurt images
		temp_list = []
		for i in range(14):
			img = pygame.image.load(f'img/{self.name}/hurt/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load deadge images
		temp_list = []
		for i in range(261):
			img = pygame.image.load(f'img/{self.name}/deadge/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load victory images
		temp_list = []
		for i in range(33):
			img = pygame.image.load(f'img/{self.name}/victory/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		animation_cooldown = 33
		#Handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks() 
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()

	def idle(self):
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def attack(self, target):
		#deal damage to enemy
		rand = random.randint(-5, 5)
		damage = self.strength + rand
		target.hp -= damage
		#run enemy hurt animation
		target.hurt()
		#check if target has died
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)
		
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def hurt(self):
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def victory(self):
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()		
	
	def reset(self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

	def draw(self):
			screen.blit(self.image, self.rect)	



#Demon class
class Demon():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0 #0:idle, 1:intro, 2:attack, 3:attack v2, 4: attack v3 5: attack v4, 6: Cry, 7: Hurty, 8: Baby, 9: RIPBOZO, 10: Victory
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(106):
			img = pygame.image.load(f'img/Lucy/IdleHR/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.8, img.get_height() * 0.8))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load intro images
		temp_list = []
		for i in range(88):
			img = pygame.image.load(f'img/Lucy/Intro/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load LaserAttack images
		temp_list = []
		for i in range(76):
			img = pygame.image.load(f'img/Lucy/Laser/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 1.1, img.get_height() * 1.1))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load AngyAttack images
		temp_list = []
		for i in range(93):
			img = pygame.image.load(f'img/Lucy/Angy/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 1.1, img.get_height() * 1.1))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load AngyV2Attack images
		temp_list = []
		for i in range(61):
			img = pygame.image.load(f'img/Lucy/Angy2S/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.8, img.get_height() * 0.8))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load FireAttack images
		temp_list = []
		for i in range(144):
			img = pygame.image.load(f'img/Lucy/Fire/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 1.1, img.get_height() * 1.1))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load cry images
		temp_list = []
		for i in range(159):
			img = pygame.image.load(f'img/Lucy/Cry/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.6, img.get_height() * 0.6))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load Hurty images
		temp_list = []
		for i in range(153):
			img = pygame.image.load(f'img/Lucy/Hurty/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.7, img.get_height() * 0.7))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load Baby images
		temp_list = []
		for i in range(134):
			img = pygame.image.load(f'img/Lucy/Baby/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.93, img.get_height() * 0.93))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load RIPBOZO images
		temp_list = []
		for i in range(552):
			img = pygame.image.load(f'img/Lucy/RIPBOZOnobg/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 1.1, img.get_height() * 1.1))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load victory images
		temp_list = []
		for i in range(150):
			img = pygame.image.load(f'img/Lucy/victory/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.7, img.get_height() * 0.7))
			temp_list.append(img)
		self.animation_list.append(temp_list)																
		self.image = self.animation_list[self.action][self.frame_index]
#		self.rect = pygame.Rect(x, y, img.get_width(), img.get_height())
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		animation_cooldown = 20
		#Handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 9:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()

	def idle(self):
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def attack(self, target):
		#deal damage to enemy
		rand = random.randint(-5, 5)
		damage = self.strength + rand
		target.hp -= damage
		#run enemy hurt animation
		target.hurt()
		#check if target has died
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)
		

		#roll for attack animation
		randatk = random.randint(2, 5)
		#set variables to attack animation
		self.action = randatk
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()
	
	def intro(self):
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def death(self):
		self.action = 9
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def hurt(self):
		#roll for hurt animation
		randhurt = random.randint(6, 8)
		self.action = randhurt
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
	
	def reset(self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

	def draw(self):
			screen.blit(self.image, self.rect)	

#fighter class
class wiggly():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(22):
			img = pygame.image.load(f'img/wiggly/idle/slowedfaster/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.2, img.get_height() * 0.2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(11):
			img = pygame.image.load(f'img/wiggly/attack/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.2, img.get_height() * 0.2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load death images
		temp_list = []
		for i in range(36):
			img = pygame.image.load(f'img/wiggly/deadge/{i}.gif')
			img = pygame.transform.scale(img, (img.get_width() * 0.2, img.get_height() * 0.2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def update(self):
		animation_cooldown = 30
		#Handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 2:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()

	def idle(self):
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def attack(self, target):
		#deal damage to enemy
		rand = random.randint(-5, 5)
		damage = self.strength + rand
		target.hp -= damage
		#run enemy hurt animation
		target.hurt()
		#check if target has died
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)
		
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def hurt(self):
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	
	
	def reset(self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

	def draw(self):
			screen.blit(self.image, self.rect)	

#draw Special rect
class Special():
	def __init__(self, x, y):
		self.animation_list = []
		self.frame_index = 0
		self.frame_counter = 0
		self.action = 0  #0: OneGuy, 1: Sussy, 2: Corpa, 3:Marriage, 4:Moderating, 5:Gayge
		self.update_time = pygame.time.get_ticks()
		#load OneGuy images
		temp_list = []
		for i in range(142):
			img = pygame.image.load(f'img/Specials/OneGuy/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load Sussy images
		temp_list = []
		for i in range(142):
			img = pygame.image.load(f'img/Specials/Sussy/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load Corpa images
		temp_list = []
		for i in range(77):
			img = pygame.image.load(f'img/Specials/Corpa/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load Marriage images
		temp_list = []
		for i in range(291):
			img = pygame.image.load(f'img/Specials/Marriage/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load Moderating images
		temp_list = []
		for i in range(110):
			img = pygame.image.load(f'img/Specials/Moderating/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load Gayge images
		temp_list = []
		for i in range(153):
			img = pygame.image.load(f'img/Specials/Gayge/{i}.gif')
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def update(self):
		animation_cooldown = 30
		#Handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
			self.frame_counter +=1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			self.frame_index = len(self.animation_list[self.action]) - 1
			self.rect.center = 1000,800

	def PlayOneGuy(self):
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def PlaySussy(self):
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def PlayCorpa(self):
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def PlayMarriage(self):
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def PlayModerating(self):
		self.action = 4
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	

	def PlayGayge(self):
		self.action = 5
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()	


	def draw(self):
			screen.blit(self.image, self.rect)	



class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp
	
	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 250, 20))
		pygame.draw.rect(screen, white, (self.x, self.y, 250*ratio, 20))

#Same as above but diffent sizes
class wigglyHealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp
	
	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, white, (self.x, self.y, 150*ratio, 20))

#Same as above but diffent sizes
class BossHealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp
	
	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 300, 20))
		pygame.draw.rect(screen, white, (self.x, self.y, 300*ratio, 20))		
		
class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0

	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()

damage_text_group = pygame.sprite.Group()


wiggly1 = wiggly(530, 330, 'Wiggly', 5, 6, 1)
wiggly2 = wiggly(730, 330, 'Wiggly', 5, 6, 1)
ratJAM1 = ratJAM(200,305,'ChatRat', 30, 12, 3)
LucyPyre = Demon(800,400, 'Lucy', 69, 10, 0)
special = Special(1000,800)
				#original LucyPyre coordinates630, 192,
	
wiggly_list = []
wiggly_list.append(wiggly1)
wiggly_list.append(wiggly2)

ratJAM_health_bar = HealthBar(100, screen_height - bottom_panel + 60, ratJAM1.hp, ratJAM1.max_hp)
wiggly1_health_bar = wigglyHealthBar(435, screen_height - bottom_panel + 60, wiggly1.hp, wiggly1.max_hp)
wiggly2_health_bar = wigglyHealthBar(620, screen_height - bottom_panel + 60, wiggly2.hp, wiggly2.max_hp)
Lucy_health_bar = BossHealthBar(450, screen_height-bottom_panel+ 60, LucyPyre.hp, LucyPyre.max_hp)

#create buttons
potion_button = Button(screen, 23, screen_height - bottom_panel + 40, potion_img, 64, 64)
restart_button = Button(screen, 277, 120, restart_img, 220, 50)
special_button = Button(screen, 270, 450, restart_img, 120, 30)

run = True
runboss = False
intro_event = 0
while run: 

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	ratJAM_health_bar.draw(ratJAM1.hp)
	wiggly1_health_bar.draw(wiggly1.hp)
	wiggly2_health_bar.draw(wiggly2.hp)
	


	#draw Fighters
	
	ratJAM1.update()
	ratJAM1.draw()
	for wiggly in wiggly_list:
		wiggly.update()
		wiggly.draw()
	#draw the damage text
	damage_text_group.update()
	damage_text_group.draw(screen)


	#control player actions
	#reset action variables
	attack = False
	potion = False
	target = None
	#make sure mouse is Visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, wiggly in enumerate(wiggly_list):
		if wiggly.rect.collidepoint(pos):
			#hide mouse
			pygame.mouse.set_visible(False)
			#show sword
			screen.blit(sword_img, pos)
			if clicked == True and wiggly.alive == True:
				attack = True
				target = wiggly_list[count]


	if potion_button.draw():
		potion = True
	#show number of potions remaining
	draw_text('Potions: '+ str(ratJAM1.potions), font, white, 100, screen_height - bottom_panel + 80)

	if game_over == 0:
		#player action
		if ratJAM1.alive == True:
			if current_fighter == 1 and intro_event!= 1 and Boss_turn == 0:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#look for player action
					#attack
					if attack == True and target != None and target!=LucyPyre:
						ratJAM1.attack(target)
						current_fighter += 1
						action_cooldown = 0
					#potion
					if potion == True:
						if ratJAM1.potions > 0:
							#check if potion would heal the player beyond max health
							if ratJAM1.max_hp - ratJAM1.hp > potion_effect:
								heal_ammount = potion_effect
							else:
								heal_ammount = ratJAM1.max_hp - ratJAM1.hp
							ratJAM1.hp += heal_ammount
							ratJAM1.potions -= 1
							damage_text = DamageText(ratJAM1.rect.centerx, ratJAM1.rect.y, str(heal_ammount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0



		#enemy action
		for count, wiggly in enumerate(wiggly_list):
			if current_fighter == 2 + count:

				if wiggly.alive == True:
					action_cooldown +=1
					if action_cooldown >= action_wait_time:
						#check if wiggly needs to heal first
						if (wiggly.hp / wiggly.max_hp) < 0.5 and wiggly.potions > 0:
							#potion
							#check if potion would heal the wiggly beyond max health
							if wiggly.max_hp - wiggly.hp > potion_effect:
								heal_ammount = potion_effect
							else:
								heal_ammount = wiggly.max_hp - wiggly.hp
							wiggly.hp += heal_ammount
							wiggly.potions -= 1
							damage_text = DamageText(wiggly.rect.centerx, wiggly.rect.y, str(heal_ammount), green)
							damage_text_group.add(damage_text)						
							current_fighter += 1
							action_cooldown = 0

						#attack
						else:
							wiggly.attack(ratJAM1)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter += 1

		#if all fighters have had a turn then reset
		if current_fighter > total_fighters:
			current_fighter = 1

	#check if all wigglys are dead
	alive_wigglys = 0
	for wiggly in wiggly_list:
		if wiggly.alive == True:
			alive_wigglys += 1
	if alive_wigglys== 0:
		pygame.draw.rect(screen, black, [430, 415, 350, 70])
		attack = False
		potion = False
		target = None
		total_fighters = 2
		rat_turn = 1
		
		draw_text(str(randname), font, white, 450, (screen_height - bottom_panel) + 30 )
		draw_text(f'HP: {LucyPyre.hp}', font, white, 680, (screen_height - bottom_panel) + 30 )
		Lucy_health_bar.draw(LucyPyre.hp)
		LucyPyre.update()

		#Check if intro has played before
		if intro_event == 0:
			#play the intro animation and change Lucy's rectangle postion
			LucyPyre.action = 1
			LucyPyre.rect.topleft = 0, 0
			intro_event = intro_event + 1

		#Check if the intro has played and start the cooldown before next action and also reset Lucy's position
		if intro_event == 1:
			current_fighter = 0
			intro_cooldown += 1
			if intro_cooldown > intro_wait_time:
				current_fighter =1
				intro_event += 1
				LucyPyre.rect.center = 630, 192
			
		#Change Lucy's position once attack animation begins and reset her postion
		if LucyPyre.action == 2:
			LucyPyre.rect.center = 530, 192
		if LucyPyre.action == 3:
			LucyPyre.rect.center = 530, 192
		if LucyPyre.action == 4:
			LucyPyre.rect.center = 530, 202
		if LucyPyre.action == 5:
			LucyPyre.rect.center = 530, 206
		if LucyPyre.action == 6:
			LucyPyre.rect.center = 530, 167
		if LucyPyre.action == 7:
			LucyPyre.rect.center = 570, 175
		if LucyPyre.action == 8:
			LucyPyre.rect.center = 570, 170
		if LucyPyre.action == 9:
			LucyPyre.rect.center = 400, 170													
		if LucyPyre.action == 0 and intro_event == 2:
			LucyPyre.rect.center = 630, 192
		LucyPyre.draw()
		special.update()
		special.draw()



		if LucyPyre.rect.collidepoint(pos) and alive_wigglys == 0:
			#hide mouse
			pygame.mouse.set_visible(False)
			#show sword
			screen.blit(sword_img, pos)
			if boss_clicked == True and alive_wigglys == 0:
					boss_attack = True
					boss_target = LucyPyre
		
		#create boss_clicked and boss_attack
		#make it so 1st RatJam Turn check target CANNOT be LucyPyre

		if ratJAM1.alive == True:
			if rat_turn == 1 and intro_event != 1:
				rat_counter += 1
				if rat_counter >= boss_wait_time:
					#look for player action
					#attack 
					if boss_attack == True and boss_target == LucyPyre and LucyPyre.alive == True:
						boss_clicked= False
						ratJAM1.attack(LucyPyre)
						boss_attack = False
						
						rat_turn = 0
						rat_counter = 0
						Boss_counter = 0
						Boss_turn = 1
					#potion
					if potion == True:
						if ratJAM1.potions > 0:
							#check if potion would heal the player beyond max health
							if ratJAM1.max_hp - ratJAM1.hp > potion_effect:
								heal_ammount = potion_effect
								rat_turn = 0
								rat_counter = 0
								Boss_counter = 0
								Boss_turn = 1
							else:
								heal_ammount = ratJAM1.max_hp - ratJAM1.hp
								ratJAM1.hp += heal_ammount
								ratJAM1.potions -= 1
								damage_text = DamageText(ratJAM1.rect.centerx, ratJAM1.rect.y, str(heal_ammount), green)
								damage_text_group.add(damage_text)
							rat_turn  = 0
							rat_counter = 0
							Boss_counter = 0
							Boss_turn = 1
			 #enemy action
				if Boss_turn == 1 and LucyPyre.alive == True:
					Boss_counter += 1
					if Boss_counter >= boss_wait_time:
							LucyPyre.attack(ratJAM1)
							Boss_turn = 0
							Boss_counter = 0
							rat_counter = 0
							rat_turn = 1
							
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					boss_clicked = True
				else: 
					boss_clicked = False
		else:
			LucyPyre.action = 10
			LucyPyre.rect.center = 490, 160
			if frameset == 0:
				special.action = 3
				special.rect.center = 400,200
				special.frame_index = 0
				frameset = 1
			if frameset == 1:
					special_counter_timer = special_counter_timer+1
			if special.action == 3:
				special_wait_time = 540					
			if special_counter_timer >= special_wait_time:	
				frameset=2
				game_over = -1	
	if LucyPyre.alive==False:
		ratJAM1.action = 4
		if frameset == 0:
			randlist = [0,1,2,4,5]
			randa = random.choice(randlist)
			special.action = randa
			special.rect.center = 400,200
			special.frame_index = 0
			frameset = 1
		if frameset == 1:
			special_counter_timer = special_counter_timer+1
		if special.action ==  0:
			special_wait_time = 240
		if special.action == 1:
			special_wait_time = 240
		if special.action == 2:
			special_wait_time = 140
		if special.action == 4:
			special_wait_time = 200
		if special.action == 5:
			special_wait_time = 269							
		if special_counter_timer >= special_wait_time:	
			game_over = 1
			frameset=2
	#check if game is over
	if game_over != 0:
		if game_over == 1 and frameset==2:
			screen.blit(victory_img, (250, 50))
		if game_over == -1 and frameset==2:
			screen.blit(defeat_img, (150, 20))
		if restart_button.draw():
			#redefine game variables
			ratJAM1.reset()
			LucyPyre.reset()
			for wiggly in wiggly_list:
				wiggly.reset()
			intro_event = 0
			LucyPyre.rect.topleft = 0, 0
			LucyPyre.action == 0
			action_cooldown = 0 
			game_over = 0
			frameset=0
			current_fighter = 1
			total_fighters = 3
			Boss_turn = 0
			Boss_counter = 0
			rat_turn = 0
			rat_counter = 0
			action_cooldown = 0
			action_wait_time=90
			boss_wait_time = 170
			intro_cooldown = 0
			intro_wait_time=156
			special_counter_timer = 0
			special_wait_time = 156
			boss_attack = False
			boss_clicked = False
			attack = False
			potion = False
			boss_target = None 
			potion_effect = 15
			clicked = False
			game_over = 0
			frameset = 0
			special.rect.center =1000,800
			randname = random.choice(Lucynamelist) 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else: 
			clicked = False

	pygame.display.update()

pygame.quit()