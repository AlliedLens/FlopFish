import pygame
from pygame.locals import *
import sys
import random
pygame.init()


# CONSTANTS


FPS = 120
WIDTH = 512
HEIGHT = 1024
SCREENSPEED = -1
GRAVITY = 0.11
PILLARSPEED = -2.5
PILLARTIME = 3000 # time taken between spawning 
PILLARGAP = 300 # gap between bottom and top pillars
JUMPSPEED = 25 
# variables

angle = 0
score = 0
highScore = 0
framesPassedSinceScore = 0




# BOOLS, and OTHERS

floorRect = pygame.Rect(0, 944, WIDTH, 200) # a Rect object of the floor, to check for collisions
dormantScreen = False
pillarList = []
PILLARSPAWN = pygame.USEREVENT # similar to events in event loop, except that it is triggered by a timer, shown in a timer below
pygame.time.set_timer(PILLARSPAWN, PILLARTIME)
bottomPillarHeightList = list(range(400, 900, 75))
random.shuffle(bottomPillarHeightList)

# ASSETS

fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT)) # creating dimensions of the surface object
pygame.display.set_caption('FloppyFish')

bgSurface1 = pygame.image.load('assets/OceanBackground(512x1024).png').convert() # loading the background images that are played continously in the background
bgSurface2 = pygame.image.load('assets/OceanBackground(512x1024)-2.png').convert()	

floor1 = pygame.image.load('assets/floor-1.png').convert() # loading the colorful floor images that are played continously in the background
floor2 = pygame.image.load('assets/floor-2.png').convert()

yellowFishMid = pygame.image.load('assets/yellowFishMid.png').convert_alpha()
yellowFishUp = pygame.image.load('assets/yellowFishUp.png').convert_alpha()
yellowFishDown = pygame.image.load('assets/yellowFishDown.png').convert_alpha()


grayFishMid = pygame.image.load('assets/GrayFishMid.png').convert_alpha()
grayFishUp = pygame.image.load('assets/GrayFishUp.png').convert_alpha()
grayFishDown = pygame.image.load('assets/GrayFishDown.png').convert_alpha()

blueFishMid = pygame.image.load('assets/BlueFishMid.png').convert_alpha()
blueFishUp = pygame.image.load('assets/BlueFishUp.png').convert_alpha()
blueFishDown = pygame.image.load('assets/BlueFishDown.png').convert_alpha()

pillarTop = pygame.image.load('assets/PillarTop.png').convert_alpha()
pillarBottom = pygame.image.load('assets/PillarBottom.png').convert_alpha()

gameFont = pygame.font.Font("04B_19.ttf", 40)

# CLASSES



class background: # a class that keeps track of the x position of each background Image,  and puts it at the beginning of the screen the moment it completely passes thorugh the visible part of the screen
	x = 0
	
	def __init__(self, x):
		self.x = x

	def moveScreen(self, delX): # moves the x coord of the bg object by an amount delX 
		self.x += delX
		if self.x <= -WIDTH:
			self.x = WIDTH

screen1 = background(0)
screen2 = background(WIDTH)

class fish: # a class that keeps track of the y position of the fish, and any changes made to it
	
	def __init__(self, y, orientation, colour):
		self.y = y
		self.velocity = 0
		self.orientation = orientation
		self.colour = colour   
								# TL X, TL Y, width, height
		self.rect = pygame.Rect(30, self.y, 68, 48)


	def moveFish(self, jump): # jump is a boolean that tells if the fish has jumped, if the fish has jumped, Velocity is reset to 0
		global dormantScreen, angle
		if (self.rect).colliderect(floorRect): # if the fish collides with the floor , ceiling, or Pillar, end game
			dormantScreen = True
			pillarList.clear()
		
		for pillar in pillarList:
			if (self.rect).colliderect(pillar.rect):
				dormantScreen = True
				pillarList.clear()
		
		if jump and not dormantScreen:
			self.velocity = -4
		
		if not dormantScreen:
			self.velocity += GRAVITY	
			self.y += self.velocity	
			self.rect = pygame.Rect(30, self.y, 68, 48)

		if dormantScreen:
			self.y = HEIGHT//2
			self.rect = pygame.Rect(30, self.y, 68, 48)
			self.velocity = 0
			angle = 0

class pillar:
	def __init__(self, x, y, img): # the top left and top right coords, and the val that determines whether it is a top or bottom pillar
		self.y = y
		self.x = x
		self.img = img # Top or Bottom
		self.rect = pygame.Rect(self.x, self.y, 96, 640)
	
	def movePillar(self):
		if self.x > -100:
			self.x += PILLARSPEED
			self.rect = pygame.Rect(self.x, self.y, 96, 640)

fishColors = ["gray", "yellow", "blue"]
random.shuffle(fishColors)

fish = fish(HEIGHT//2, "Mid", fishColors[0])



# FUNCTIONS
def main():
	global score, framesPassedSinceScore, dormantScreen
	
	while True:
		for event in pygame.event.get():
			
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			if event.type == KEYDOWN and event.unicode == " ":
				fish.moveFish(jump = True)
			
			if event.type == PILLARSPAWN and not dormantScreen:
				gapList = [250, 300, 350]
				bottomHeight = bottomPillarHeightList[random.randint(0,len(bottomPillarHeightList) - 1)]
				pillarList.append(pillar(WIDTH, bottomHeight, "Bottom")) # bottom pillar
				random.shuffle(gapList)
				pillarList.append(pillar(WIDTH, bottomHeight - 600 - gapList[0], "Top")) 
			
			if event.type == KEYDOWN and event.unicode == "e" and dormantScreen:
				dormantScreen = False
		
		screenMovement()
		if not dormantScreen:
			drawPillar()
		scoreShow ()
		scoreCheck(score)
		drawFish()

		pygame.display.update()
		framesPassedSinceScore += 1
		fpsClock.tick(FPS)



def screenMovement():
	global screen1, screen2	


	DISPLAYSURF.blit(bgSurface1, (screen1.x, 0))
	DISPLAYSURF.blit(bgSurface2, (screen2.x, 0))			
	DISPLAYSURF.blit(floor1, (screen1.x, 944))
	DISPLAYSURF.blit(floor2, (screen2.x, 944))	
	screen1.moveScreen(SCREENSPEED) # the images are moved by the constant SCREENSPEED 
	screen2.moveScreen(SCREENSPEED)

def rotateFish(surface, angle):
	rotatedFish = pygame.transform.rotozoom(surface,angle,1)
	return rotatedFish

def drawFish():
	global angle
	angle += 1
	drawnFish = eval(f"{fish.colour}Fish{fish.orientation}")
	angle = fish.velocity * -10 if fish.velocity > 0 else 45
	rotatedFish = rotateFish(drawnFish, angle)
	fish.moveFish(jump = False)
	if dormantScreen:
		DISPLAYSURF.blit(drawnFish , (30, HEIGHT//2))
		return None
	DISPLAYSURF.blit(rotatedFish , (30, fish.y))



def drawPillar():
	global pillarList
	pillarList = [pillar for pillar in pillarList if pillar.x > -100] 
	for Pillar in pillarList:
		Pillar.movePillar()
		DISPLAYSURF.blit(eval(f"pillar{Pillar.img}"), (Pillar.x, Pillar.y))

def scoreCheck(score):
	scoreSurface = gameFont.render(str(int(score)) , True, (255,255,255))
	scoreRect = scoreSurface.get_rect(center = (WIDTH//2,100))
	
	highScoreSurface = gameFont.render(str(int(highScore)) , True, (255,255,255))
	highScoreRect = highScoreSurface.get_rect(center = (WIDTH//2, 150))
	
	dormantScreenText = gameFont.render("Fish Flop", True, (255,255,255))
	dormantScreenTextRect = dormantScreenText.get_rect(center = (WIDTH//2, HEIGHT *2//3))
	if not dormantScreen:	
		DISPLAYSURF.blit(scoreSurface, scoreRect)
	if dormantScreen:
		DISPLAYSURF.blit(highScoreSurface, highScoreRect)
		DISPLAYSURF.blit(dormantScreenText, dormantScreenTextRect)

def scoreShow(): 
	global score, framesPassedSinceScore, highScore
	for pillar in pillarList:
		if framesPassedSinceScore > 50:
			if 101 < (pillar.rect).centerx < 103:
				score += 1
				framesPassedSinceScore = 0
	
	if dormantScreen:
		if highScore < score:
			highScore = int(score)
		score = 0
main()