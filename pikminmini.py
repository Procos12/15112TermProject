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
#class 

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
        #The center is stored so the coordinates don't change
        #as the image changes
        center=self.rect.center
        #Changing the image of the sprite depending on the direction
        if direction=="Up":
            self.image=self.imageList["Up"]
        elif direction=="Down":
            self.image=self.imageList["Down"]
        elif direction=="Right":
            self.image=self.imageList["Right"]
        elif direction=="Left":
            self.image=self.imageList["Left"]
        #Rearranging the coordinates so that
        #the image is not moved after a change in direciton
        self.rect=self.image.get_rect()
        self.rect.center=center

    def move(self, direction):
    #This is method controls the movement of the main character
        #Depending on the direction,
        #The character's image may change, and the character
        #moves accordingly
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
        self.update()

    def update(self):
        screen.blit(self.image, self.rect)

class Pikmin():
#This class defines the pikmin. Pikmin can follow the character,
#attack enemies, die, spawn, take fruit and enemies back to the ship
#and do nothing.
    def __init__(self, spawnX=0, spawnY=0, task="Follow"):#Fix these variables later
    #This initializes the pikmin 
        self.pikmin=pg.image.load("pikmin.png")
        self.rect=self.pikmin.get_rect()
        self.rect.center=spawnX, spawnY
        self.task=task
        self.health=20
        self.target=None
        pikminList.append(self)

    def getTask(self):
    #Returns the task of the pikmin for other classes
        return self.task

    def getHealth(self):
        return self.health

    def getCoordinates(self):
        return self.rect.center[0], self.rect.center[1]

    def getDistance(self, coordinates):
    #This method is used to check whether or not the pikmin are able
    #to go to the item the player is clicking on
        #Getting the position of the object and pikmin
        objX, objY=coordinates[0], coordinates[1]
        pikX, pikY=self.getCoordinates()
        #Returning the distance between them
        return ((pikX-objX)**2+(pikY-objY)**2)**0.5

    def getSpacing(self, direction):
    #This gets the spacing of the pikmin from the player
        #This is the default spacing
        spacingX=random.randint(-20, 20)
        spacingY=random.randint(-20, 20)
        #Depending on the direction, either the x or y
        #spacing will decrease or increase
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
        pikX, pikY=self.getCoordinates()
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

    def changeTask(self, task, obj=None):
    #This method changes the task of the pikmin
        if obj!=None:
            self.target=obj
        self.task=task

    def update(self):
        screen.blit(self.pikmin, self.rect)

    def die(self):
        pikminList.remove(self)

    def getTarget(self):
        return self.target

    def goTo(self, obj=None):
    #This method tells the pikmin to go to a fruit,
    #pick it up and go to the ship when enough pikmin are
    #around the fruit
        if self.task!="goTo":
            self.task="goTo"
        if obj!=None:
            self.target=obj
        pikX, pikY=self.getCoordinates()
        targetX, targetY=self.target.getPickLocation()
        if pikX<targetX:
            self.rect.move_ip([1,0])
        if pikX>targetX:
            self.rect.move_ip([-1,0])
        if pikY>targetY:
            self.rect.move_ip([0,-1])
        if pikY<targetY:
            self.rect.move_ip([0,1])
        if pikY<targetY+25 and pikY>targetY-25:
            if pikX<targetX+25 and pikX>targetX-25:
                self.target.addPikmin(self)

    def attackEnemy(self, enemy):
        pass

class Enemy():
    def __init__(self, image, coordinates):
    #Initializing the enemy object
        self.image=pg.image.load(image)
        self.rect=self.image.get_rect()
        self.rect.center=coordinates
        self.health=100
        self.task="None"
        enemyList.append(self)
        self.pikmin=4

    def getClicked(self, mouseX, mouseY):
    #Checks if the enemy was clicked on or not
        right, left=self.rect.right, self.rect.left
        top, bottom=self.rect.top, self.rect.bottom
        if mouseX<right and mouseX>left:
            if mouseY<bottom and mouseY>top:
                return True

    def getTask(self):
        return self.task

    def getHealth(self):
        return self.health

    def decreaseHealth(self):
    #This function is used to decrease the enemy health
        self.health-=5
        if self.health<=0:
            self.task="None"

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
        self.update()

    def update(self):
        screen.blit(self.image, self.rect)

class Fruit():
#This class contains all the attributes of a fruit. Fruits can be 
#taken back to the ship and are added to the juice when they are
    FRUITS={"apple":4}
    def __init__(self, fruit, x, y, ship):
        self.image=pg.image.load(fruit+".png")
        self.rect=self.image.get_rect()
        self.task="Exist"
        self.rect.center=(x, y)
        self.fruit=fruit
        self.pikmin=Fruit.FRUITS[fruit]
        self.juice=Fruit.FRUITS[fruit]
        fruitList.append(self)
        self.pikminList=[]
        self.ship=ship
        self.shipX, self.shipY=self.ship.getCoordinates()

    def getClicked(self, mouseX, mouseY):
    #Checks if the enemy was clicked on or not
        right, left=self.rect.right, self.rect.left
        top, bottom=self.rect.top, self.rect.bottom
        if mouseX<right and mouseX>left:
            if mouseY<bottom and mouseY>top:
                return True

    def moveToShip(self):
        if self.task!="Move":
            self.task="Move"
        fruitX, fruitY=self.rect.center[0], self.rect.center[1]
        if fruitX<self.shipX:
            self.rect.move_ip([1, 0])
        if fruitX>self.shipX:
            self.rect.move_ip([-1, 0])
        if fruitY<self.shipY:
            self.rect.move_ip([0, 1])
        if fruitY>self.shipY:
            self.rect.move_ip([0, -1])
        if fruitX==self.shipX and fruitY==self.shipY:
            self.ship.takeFruit(self)

    def addPikmin(self, pik):
    #Adds pikmin to the list of those carrying the fruit
        if pik not in self.pikminList:
            self.pikminList.append(pik)
        if len(self.pikminList)==self.pikmin:
            self.moveToShip()

    def changeTask(self, task):
        self.task=task

    def getPikmin(self):
    #Returns the number of pikmin needed to carry the fruit
        return self.pikmin

    def getCoordinates(self):
    #Returns the coordinates of the object
        return self.rect.center[0], self.rect.center[1]

    def getTask(self):
        return self.task

    def getPickLocation(self):
    #This method is used to determine where the pikmin can pick up the fruit
        pickups=[]
        topleft, topright=self.rect.topleft, self.rect.topright
        bottomright, bottomleft=self.rect.bottomleft, self.rect.bottomright
        pickups.append(topleft)
        pickups.append(topright)
        pickups.append(bottomright)
        pickups.append(bottomleft)
        return random.choice(pickups)

    def getJuice(self):
        return self.juice

    def update(self):
    #Updatess the fruit on the screen
        screen.blit(self.image, self.rect)

    def pikDone(self):
        for i in self.pikminList:
            i.changeTask("Follow")

class Spaceship():
#This class has all the actions of the spaceship
    def __init__(self, coordinates):
    #Initializes the spacehip on the screen with a certain position
        self.image=pg.image.load("spaceship.png")
        self.rect=self.image.get_rect()
        self.rect.center=coordinates
        self.juice=0

    def spawnPikmin(self):
    #This function spawns pikmin around the ship
        #Getting the location where the pikmin spawn around the ship
        xDisplacement=random.randint(-30, 30)
        yDisplacement=random.randint(-30, 30)
        if xDisplacement>0:
            spawnX=self.rect.right+xDisplacement
        else:
            spawnX=self.rect.left+xDisplacement
        if yDisplacement>0:
            spawnY=self.rect.bottom+yDisplacement
        else:
            spawnY=self.rect.top+yDisplacement
        #Creating a pikmin at that location
        Pikmin(spawnX, spawnY)

    def takeFruit(self, fruit):
    #This function takes fruit in and adds it to the player's juice
        self.juice+=fruit.getJuice()
        fruit.pikDone()
        fruit.changeTask("None")

    def update(self):
        screen.blit(self.image, self.rect)

    def getCoordinates(self):
        return self.rect.center[0], self.rect.center[1]

#Setting up the level
barbol=Character((640, 360))
sunny=Spaceship((200, 120))
enemy1=Enemy("Enemy.png", (720, 640))
apple1=Fruit("apple", 600, 340, sunny)
apple2=Fruit("apple", 700, 400, sunny)
for i in range(5):
    sunny.spawnPikmin()
#GameLoop
while True:
    #Handling user input
    for event in pg.event.get():
        #Handling the closing of the game
        if event.type==pg.QUIT: 
            sys.exit()
        #Handling clicking the mouse
        if event.type==pg.MOUSEBUTTONDOWN:
            #Getting the mouse position
            mouseX, mouseY=pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]
            #Remove the two lines of code below later, these were just test spawning the pikmin
            if len(pikminList)<20:
                sunny.spawnPikmin()
            if len(pikminList)>0:
                for j in enemyList:
                    if j.getClicked(mouseX, mouseY):
                        for i in pikminList:
                            if i.getTask()=="Follow":
                                i.attackEnemy(j)
                for i in fruitList:
                    if i.getClicked(mouseX, mouseY):
                        for j in pikminList:
                            if j.getTask()=="Follow":
                                j.goTo(i)
                                j.changeTask("goTo")
                                break

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
        if i.getTask()=="goTo":
            i.goTo()
        i.update()
    #Handling enemy tasks
    for j in enemyList:
        if j.getTask()=="Move":
            #j.move()
            pass
        elif j.getTask()=="ToShip":
            pass
        j.update()
    for k in fruitList:
        if k.getTask()=="Move":
            k.moveToShip()
        elif k.getTask()=="None":
            fruitList.remove(k)
        k.update()

    #Updating the screen
    sunny.update()
    barbol.update()
    pg.display.flip()
    screen.fill(black)
    clock.tick(120)
