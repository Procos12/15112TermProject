#Abdulwahab Al-Rumaihi, andrewID:arumaihi
#Imports
import pygame as pg
import sys

#Initializing the main window
pg.init()
clock=pg.time.Clock()
black=0, 0, 0
screen=pg.display.set_mode((1280, 720))
pg.display.set_caption("Pikmin")


pikminList=[]
def createPikmin():
#This function creates a pikmin
    pikmin=pg.image.load("pikmin.png")
    pikRect=pikmin.get_rect()
    pikminList.append([pikmin, pikRect])
def followMouse(pikRect, pos):
#This function let's the pikmin follow the mouse
    pikX, pikY=pikRect.center[0], pikRect.center[1]
    mouseX, mouseY=pos[0], pos[1]
    if pikX<mouseX:
        pikRect.move_ip([1,0])
    if pikX>mouseX:
        pikRect.move_ip([-1,0])
    if pikY<mouseY:
        pikRect.move_ip([0,1])
    if pikY>mouseY:
        pikRect.move_ip([0,-1])
#This is the game loop
while True:
    screen.fill(black)
    for event in pg.event.get():
        if event.type==pg.QUIT:
            sys.exit()
        if event.type==pg.MOUSEBUTTONDOWN:
            if len(pikminList)<20:
                createPikmin()
    mPosition=pg.mouse.get_pos()
    for i in pikminList:
        followMouse(i[1], mPosition)
        screen.blit(i[0], i[1])
    pg.display.flip()