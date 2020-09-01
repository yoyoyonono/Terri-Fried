import pygame
import pygame.ftfont
import pygame.mixer
from math import sin
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
playCoinFX = False

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
    global playCoinFX
    onPlatform = False
    for i in range(4):
        if platforms[i].getHasCoin() and player.getX() + player.getWidth() - 3 > platforms[i].getCoinX() and player.getX() + 3 < platforms[i].getCoinX() + 24 and player.getY() - player.getHeight() + 3 < platforms[i].getCoinY() and player.getY() - 3 > platforms[i].getCoinY() - 24:
            addScore(1)
            platforms[i].setHasCoin(False)
            playCoinFX = True
        if player.getX() + 1 < platforms[i].getX() + platforms[i].getWidth() and player.getX() + player.getWidth() > platforms[i].getX() and player.getY() - player.getHeight() <= platforms[i].getY() and player.getY() > platforms[i].getY() - platforms[i].getHeight():
            if player.getY() > platforms[i].getY() - platforms[i].getHeight()/2:
                player.setVelocity(player.getVelocity()[0], 5)
            elif player.getY() - player.getHeight() < platforms[i].getY() - platforms[i].getHeight():
                print('set platform', True)
                onPlatform = True
                player.setY(platforms[i].getY() - player.getHeight())
                player.setY(player.getY() + 1)
    player.setOnPlatform(onPlatform)

def main():
    global titleScreen, playCoinFX
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
    wasMouse = False
    backgroundColor = (int(0.933*255), int(0.894*255), int(0.882*255), int(1.0*255))
    clickToBeginColor = (int(0.698*255), int(0.588*255), int(0.49*255), int(0.4*255))
    platformColor = (int(0.698*255), int(0.588*255), int(0.49*255), int(1.0*255))
    polyMarsColor = (int(0.835*255), int(0.502*255), int(0.353*255), int(1.0*255))
    lineColor = (int(0.906*255), int(0.847*255), int(0.788*255), int(1.0*255))
    while running:
        if titleScreen:
            if splashTimer > 120:
                if not playedSelect:
                    fxSelect.play()
                    playedSelect = True
                screen.fill(backgroundColor)
                screen.blit(logo, (int(screenWidth/2 - 200), int(screenHeight/2 - 45 - 30)))
                screen.blit(font32.render(highscore, True, (0, 0, 0)), (int(screenWidth/2 - 37), int(screenHeight/2 + 10)))
                screen.blit(font32.render('CLICK ANYWHERE TO BEGIN', True, clickToBeginColor), (int(screenWidth/2 - 134), int(screenHeight/2 + 50)))
                if pygame.mouse.get_pressed()[0]:
                    fxSelect.play()
                    titleScreen = False
                    (mouseDownX, mouseDownY) = pygame.mouse.get_pos()
            else:
                if not playedSplash:
                    fxSplash.play()
                    playedSplash = True
                screen.fill(backgroundColor)
                screen.blit(font32.render('POLYMARS', True, polyMarsColor), (int(screenWidth/2 - 54), int(screenHeight/2 - 3)))
                screen.blit(splashEggSprite, (int(screenWidth/2 - 16), int(screenHeight/2 - 16 - 23)))
                splashTimer += 1
        else:
            screen.fill(backgroundColor)
            if playCoinFX:
                fxCoin.play()
                playCoinFX = False
            if (pygame.mouse.get_pressed()[0] and not wasMouse) and player.isOnGround():
                fxClick.play()
                (mouseDownX, mouseDownY) = pygame.mouse.get_pos()
            if (not pygame.mouse.get_pressed()[0] and wasMouse) and player.isOnGround():
                if firstTime:
                    firstTime = False
                else:
                    fxLaunch.play()
                    if player.isOnPlatform():
                        player.setY(player.getY() + 1)
                    player.setVelocity(pygame.mouse.get_pos()[0]*0.8, pygame.mouse.get_pos()[1]*0.8) 
            checkPlayerCollision()
            player.updatePosition()
            if player.getY() > screenHeight:
                fxDeath.play()
                resetGame()
            [i.updatePosition() for i in platforms]
    
            lavaY = screenHeight - 43 - sin(timer) * 5
            timer += 0.05
    
            if pygame.mouse.get_pressed()[0] and player.isOnGround():
                pygame.draw.line(screen, 
                    lineColor,
                    (int(mouseDownX + (player.getX() - mouseDownX) + (player.getWidth()/2)), 
                        int(mouseDownY + (player.getY() - mouseDownY) + (player.getHeight()/2))), 
                    (int(pygame.mouse.get_pos()[0] + (player.getX() - mouseDownX) + (player.getWidth()/2)), 
                        int(pygame.mouse.get_pos()[1] + (player.getY() - mouseDownY) + (player.getHeight()/2))), 
                    3)
            
            for i in range(4):
                screen.blit(platformSprite, (platforms[i].getX(), platforms[i].getY()))
                if platforms[i].getHasCoin():
                    screen.blit(coinSprite, (int(platforms[i].getCoinX()), int(platforms[i].getCoinY())))
    
            screen.blit(playerSprite, (int(player.getX()), int(player.getY())))
            screen.blit(lavaSprite, (0, int(lavaY)))
            screen.blit(scoreBoxSprite, (17, 17))
            screen.blit(font.render(score, True, (0, 0, 0)), (28, 20))
            screen.blit(font32.render(highscore, True, (0, 0, 0)), (17, 90))
        
        wasMouse = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(60)
    return 0

if __name__ == "__main__":
    main()