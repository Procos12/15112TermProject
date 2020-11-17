#Abdulwahab Al-Rumaihi, andrewID:arumaihi
#Imports
import pygame as pg
import random
import sys

#Initial setup
pg.init()
clock=pg.time.Clock()
black=0, 0, 0
screen=pg.display.set_mode((1280, 720))
pg.display.set_caption("Pikmin")
pikminList=[]
enemyList=[]
fruitList=[]

#Classes
class Pikmin():
#This class defines the pikmin. Pikmin can follow the character,
#attack enemies, die, spawn, take fruit and enemies back to the ship
#and do nothing.
    def __init__(self, spawnX=0, spawnY=0, task="Nothing"):#Fix these variables later
    #This initializes the pikmin 
        self.pikmin=pg.image.load("pikmin.png")
        self.rect=self.pikmin.get_rect()
        self.rect.center=spawnX, spawnY
        self.task=task
        self.health=20
        pikminList.append(self)

    def getTask(self):
    #Returns the task of the pikmin for other classes
        return self.task

    def getDistance(self):
    #This method is used to check whether or not the pikmin are able
    #to go to the location you are clicking on
        mPosition=pg.mouse.get_pos()
        #Getting the position of the mouse and pikmin
        mouseX, mouseY=mPosition[0], mPosition[1]
        pikX, pikY=self.rect.center[0], self.rect.center[1]
        #Returning the distance between them
        return ((pikX-mouseX)**2+(pikY-mouseY)**2)**0.5

    def getSpacing(self, direction):
    #This gets the spacing of the pikmin from the player
        #This is the default spacing
        spacingX=random.randint(-20, 20)
        spacingY=random.randint(-20, 20)
        #Depending on the direction, either the x or y spacing will increase
        if direction=="Down":
            spacingY=random.randint(-45, -15)
        if direction=="Up":
            spacingY=random.randint(15, 45)
        if direction=="Right":
            spacingX=random.randint(-45, -15)
        if direction=="Left":
            spacingX=random.randint(15, 45)
        return spacingX, spacingY

    def followCharacter(self, char):
    #Following the main character
        #Getting the pikmin's coordinates and the characters direction
        pikX=self.rect.center[0]
        pikY=self.rect.center[1]
        direction=char.getDirection()
        #Getting the coordinates of the characters back so the pikmin follow
        if direction=="Down":
            charX, charY=char.rect.midtop[0], char.rect.midtop[1]
        if direction=="Up":
            charX, charY=char.rect.midbottom[0], char.rect.midbottom[1]
        if direction=="Right":
            charX, charY=char.rect.midleft[0], char.rect.midleft[1]
        if direction=="Left":
            charX, charY=char.rect.midright[0], char.rect.midright[1]
        #Getting the spacing and moving the pikmin accordingly
        spacingX, spacingY=self.getSpacing(direction)
        if pikX<charX+spacingX:
            self.rect.move_ip([1, 0])
        if pikX>charX+spacingX:
            self.rect.move_ip([-1, 0])
        if pikY<charY+spacingY:
            self.rect.move_ip([0, 1])
        if pikY>charY+spacingY:
            self.rect.move_ip([0, -1])
        screen.blit(self.pikmin, self.rect)

    def update(self):
        screen.blit(self.pikmin, self.rect)

    #def attackEnemy(self, enemy):

    #def takeToShip(self, item):

class Character():
#All of the attributes of the main character are under this class
    def __init__(self, coordinates):
        self.imageList={}
        self.imageList["Right"]=pg.image.load("barbolR.png")
        self.imageList["Left"]=pg.image.load("barbolL.png")
        self.imageList["Up"]=pg.image.load("barbolU.png")
        self.imageList["Down"]=pg.image.load("barbolD.png")
        self.image=self.imageList["Right"]
        self.direction="Right"
        self.rect=self.image.get_rect()
        self.rect.center=coordinates

    def getDirection(self):
        return self.direction

    def changeDirection(self, direction):
    #This method changes the direction of the main character
        self.direction=direction
        center=self.rect.center
        if direction=="Up":
            self.image=self.imageList["Up"]
        elif direction=="Down":
            self.image=self.imageList["Down"]
        elif direction=="Right":
            self.image=self.imageList["Right"]
        elif direction=="Left":
            self.image=self.imageList["Left"]
        self.rect=self.image.get_rect()
        self.rect.center=center

    def move(self, direction):
    #This is method controls the movement of the main character
        if direction=="right":
            if self.direction!="Right":
                self.changeDirection("Right")
            self.rect.move_ip([1, 0])
        elif direction=="left":
            if self.direction!="Left":
                self.changeDirection("Left")
            self.rect.move_ip([-1, 0])
        elif direction=="up":
            if self.direction!="Up":
                self.changeDirection("Up")
            self.rect.move_ip([0, -1])
        elif direction=="down":
            if self.direction!="Down":
                self.changeDirection("Down")
            self.rect.move_ip([0, 1])
        screen.blit(self.image, self.rect)

    def update(self):
        screen.blit(self.image, self.rect)

class Enemy():
#This
    def __init__(self, image, coordinates):
    #Initializing the enemy object
        self.image=pg.image.load(image)
        self.rect=self.image.get_rect()
        self.rect.center=coordinates
        self.health=100
        enemyList.append(self)

    def move(self, direction):
    #This function is used for the motion of the enemy
        if direction=="down":
            self.rect.move_ip([0,1])
        elif direction=="up":
            self.rect.move_ip([0,-1])
        elif direction=="right":
            self.rect.move_ip([1,0])
        elif direction=="left":
            self.rect.move_ip([-1,0])
        screen.blit(self.image, self.rect)

#class Fruit():

class Spaceship():
#This class 
    def __init__(self, coordinates):
    #Initializes the spacehip on the screen with a certain position
        self.image=pg.image.load("spaceship.png")
        self.rect=self.image.get_rect()
        self.rect.center=coordinates

    def spawnPikmin(self):
    #This function spawns pikmin around the ship
        #Getting the location where the pikmin spawn around the ship
        xDisplacement=random.randint()
        yDisplacement=random.randint()
        spawnX=self.rect.center[0]+xDisplacement
        spawnY=self.rect.center[1]+yDisplacement
        #Creating a pikmin at that location
        Pikmin(spawnX, spawnY)

#Setting up the level
barbol=Character((640, 360))
#GameLoop
while True:
    #Handling user input
    for event in pg.event.get():
        if event.type==pg.QUIT: 
            sys.exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            if len(pikminList)<20:
                Pikmin(640, 360, "Follow")
    movement=pg.key.get_pressed()
    if movement[pg.K_a]:
        barbol.move("left")
    elif movement[pg.K_d]:
        barbol.move("right")
    elif movement[pg.K_w]:
        barbol.move("up")
    elif movement[pg.K_s]:
        barbol.move("down")
    #Handling pikmin tasks
    for i in pikminList:
        if i.getTask()=="Follow":
            i.followCharacter(barbol)
        if i.getTask()=="Nothing":
            i.update()
    #Updating the screen
    barbol.update()
    pg.display.flip()
    screen.fill(black)
    clock.tick(120)
