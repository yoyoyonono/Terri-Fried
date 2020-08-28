from random import randint
screenHeight = 450

class Platform:
    def __init__(self, index):
        self.width = 100
        self.height = 32
        self.x = randint(20, 680)
        self.y = 0 - self.height - (index * 100)
        self.coinInt = randint(0, 3)
        self.hasCoin = (0 in [self.coinInt, index])
        self.coinX = self.x + self.width/2 - 24/2
        self.coinY = self.y - 24 - 5
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getHasCoin(self):
        return self.hasCoin
    
    def setHasCoin(self, value):
        self.hasCoin = value
    
    def getCoinX(self):
        return self.coinX
    
    def getCoinY(self):
        return self.coinY
    
    def updatePosition(self):
        global screenHeight
        self.y += 1
        self.coinX = self.x + self.width/2 - 24/2
        self.coinY = self.y - 24 - 5
        if self.y > screenHeight:
            self.x = randint(20, 680)
            self.y = 0 - self.height
            self.hasCoin = (not self.cointInt == 0)