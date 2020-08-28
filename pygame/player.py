gravity = 1

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onPlatform = False
        self.velocity = [0,0]
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def isOnGround(self):
        return self.onPlatform
    
    def isOnPlatform(self):
        return self.onPlatform
    
    def setOnPlatform(self, result):
        self.onPlatform = result

    def getVelocity(self):
        return self.velocity

    def setVelocity(self, x, y):
        self.velocity = [x,y]
    
    def updatePosition(self):
        global gravity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if not self.isOnGround():
            self.velocity[1] += gravity
        else:
            velocity = [0,0]
        
        if self.x < 0:
            self.velocity[0] *= 1

        if self.x + self.width > 800:
            self.velocity[0] *= -1 