#These are some methods/functions I had initially planned to implement, but could not.
    def faceMouse(self):
        mPosition=pg.mouse.get_pos()
        mouseX, mouseY=mPosition[0], mPosition[1]
        mainX, mainY=self.rect.left+32, self.rect.top+30
        x=mouseX-mainX
        y=mouseY-mainY
        
    def faceMouse(self):
        #angle=self.calculateAngle(mouseX, mouseY)
        self.sprite=pg.transform.rotate(self.sprite, 30)
        self.rect=self.sprite.get_rect()
        screen.blit(self.sprite, self.rect)

    #def calculateAngel(self, mouseX, mouseY):

    #def takeDamage(self):
        #if self.health<=0:
            #pikminList.remove(self)

    def identifyTask(self):
        