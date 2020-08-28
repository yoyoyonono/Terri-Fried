import pygame
import pygame.ftfont
import pygame.mixer
from player import Player
from platform1 import Platform

pi = 3.1415926535897
gravity = 1
platforms = [Platform(x) for x in range(4)]
player = Player(platforms[0].getX() + platforms[0].getWidth()/2 - 26 / 2, platforms[0].getY() - platforms[0].getHeight(), 26, 32)

scoreInt = 0
highScoreInt = 0 # add in file loading
score = ''
highscore = ''

titleScreen = True
playCoinFx = False

def addScore(amount: int):
    global scoreInt, highScoreInt
    scoreInt += amount
    score = str(scoreInt).zfill(3)
    if scoreInt > highScoreInt:
        highScoreInt = scoreInt
        highscore = 'BEST: ' + str(highScoreInt)

def resetScore():
    global scoreInt, score
    scoreInt = 0
    score = '000'
    #SaveStorageValue(0, highscoreInt);
    
def resetGame():
    global platforms
    resetScore()
    for i in range(4):
        platforms[i] = Platform(i)
    
    player.setVelocity(0, 0)
    player.setX(platforms[0].getX() + platforms[0].getWidth()/2 - 26/2)
    player.setY(platforms[0].getY() - player.getHeight())

def checkPlayerCollision():
    onPlatform = False
    for i in range(4):
        if platforms[i].getHasCoin() and player.getX() + player.getWidth() - 3 > platforms[i].getCoinX() and player.getX() + 3 < platforms[i].getCoinX() + 24 and player.getY() + player.getHeigh() - 3 > platforms[i].getcoinY() and player.getY + 3 < platforms[i].getCoinY() + 24:
            addScore(1)
            platforms[i].setHasCoin(False)
            playCoinFX = True
        if player.getX() + 1 < platforms[i].getX() + platforms[i].getWidth() and player.getX() + player.getWidth() > platforms[i].getX() and player.getY() + player.getHeight() >= platforms[i].getY() and player.getY() < platforms[i].getY() + platforms[i].getHeight():
            if player.getY() > platforms[i].getY() + platforms[i].getHeight()/2:
                player.setVelocity(player.getVelocity()[0], 5)
            elif player.getY() + player.getHeight() < platforms[i].getY() + platforms[i].getHeight():
                onPlatform = True
                player.setY(platforms[i].getY() - player.getHeight())
    player.setOnPlatform(onPlatform)

def main():
    global titleScreen
    resetScore()
    highscore = 'BEST: ' + str(highScoreInt)
    screenWidth = 800
    screenHeight = 450

    mouseDownX = 0
    mouseDownY = 0
    lavaY = screenHeight - 32
    timer = 0
    splashTimer = 0
    firstTime = True
    playedSplash = False
    playedSelect = False
    pygame.init()
    egg = pygame.image.load('resources/egg.png')
    pygame.display.set_icon(egg)
    pygame.display.set_caption('Terri-Fried')
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    playerSprite = pygame.image.load('resources/egg.png').convert_alpha()
    lavaSprite = pygame.image.load('resources/lava.png').convert_alpha()
    platformSprite = pygame.image.load('resources/platform.png').convert_alpha()
    coinSprite = pygame.image.load('resources/coin.png').convert_alpha()
    scoreBoxSprite = pygame.image.load('resources/scorebox.png').convert_alpha()
    logo = pygame.image.load('resources/logo.png').convert_alpha()
    splashEggSprite = pygame.image.load('resources/splash_egg.png').convert_alpha()

    fxLaunch = pygame.mixer.Sound('resources/launch.wav')
    fxClick = pygame.mixer.Sound('resources/click.wav')
    fxDeath = pygame.mixer.Sound('resources/die.wav')
    fxCoin = pygame.mixer.Sound('resources/coin.wav')
    fxSplash = pygame.mixer.Sound('resources/splash.wav')
    fxSelect = pygame.mixer.Sound('resources/select.wav')
    font = pygame.ftfont.Font('resources/font.otf', 64)
    font32 = pygame.ftfont.Font('resources/font.otf', 32)
    running = True

    #my own variables for optimization purposes
    clock = pygame.time.Clock()
    backgroundColor = (int(0.933*255), int(0.894*255), int(0.882*255), int(1.0*255))
    clickToBeginColor = (int(0.698*255), int(0.588*255), int(0.49*255), int(0.4*255))
    polyMarsColor = (int(0.835*255), int(0.502*255), int(0.353*255), int(1.0*255))
    while running:
        if titleScreen:
            if splashTimer > 120:
                if not playedSelect:
                    fxLaunch.play()
                    playedSelect = True
                screen.fill(backgroundColor)
                screen.blit(logo, (screenWidth/2 - 200, screenHeight/2 - 45 - 30))
                screen.blit(font32.render(highscore, True, (0, 0, 0)), (screenWidth/2 - 37, screenHeight/2 + 10))
                screen.blit(font32.render('CLICK ANYWHERE TO BEGIN', True, clickToBeginColor), (screenWidth/2 - 134, screenHeight/2 + 50))
                if pygame.mouse.get_pressed():
                    fxSelect.play()
                    titleScreen = False
                    (mouseDownX, mouseDownY) = pygame.mouse.get_pos()
            else:
                if not playedSplash:
                    fxSplash.play()
                    playedSplash = True
                screen.fill(backgroundColor)
                screen.blit(font32.render('POLYMARS', True, polyMarsColor), (screenWidth/2 - 54, screenHeight/2 + 3))
                screen.blit(splashEggSprite, (screenWidth/2 - 16, screenHeight/2 - 16 - 23))
                splashTimer += 1
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(60)
    return 0

if __name__ == "__main__":
    main()