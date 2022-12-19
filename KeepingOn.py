import pygame
from pygame.locals import *
import random
import math
import sys

XSIZE = 600
YSIZE = 400
XSPACING = 50
YSPACING = 50
YSMALLSPACING = 30
ROADSIZE = 200
MINY = YSPACING
ROADLEFTX = XSIZE
TOPSTART = (0, YSPACING * 3)
TOPEND = (ROADLEFTX, YSPACING * 3)
TOPLEFT = (0, YSMALLSPACING)
TOPRIGHT = (XSIZE, YSMALLSPACING)
MOVEAMOUNT = 15
BOTTOMLEFT = (0, YSIZE)
BOTTOMRIGHT = (XSIZE, YSIZE)
CHANGECHANCE = 10
MAXCARSPEED = 20
CARSPEEDCHANGE = 0.2
STARTSPEED = 2

WALLCOLOUR = (10,10,10, 255)

PLAYERPOS = (XSPACING, YSIZE/2)


class KeepingOn:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Keeping On")
                
        self.clock = pygame.time.Clock()

        #Load assets
        self.car = pygame.image.load('Assets/car.png')
        self.car2 = pygame.image.load('Assets/car2.png')
        self.car3 = pygame.image.load('Assets/car3.png')

        self.screen = pygame.display.set_mode((XSIZE, YSIZE))

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((140,255,140))

        self.running = True

        #Variables for controlling difficulty
        self.speed = 2
        self.roadSize = ROADSIZE
        self.changeChance = CHANGECHANCE

        self.roadPoses = [TOPSTART,TOPEND]
        self.roadBotPoses = [(TOPSTART[0], TOPSTART[1] + self.roadSize), (TOPEND[0], TOPEND[1] + self.roadSize)]

        self.carSpeed = 0

        self.carAnimCount = 0

        self.score = 0
        self.startTime = math.floor(pygame.time.get_ticks()/1000)

        #Make sure we're drawing from the middle of the car
        self.carPos = PLAYERPOS[0], PLAYERPOS[1]

        if pygame.font:
            self.font = pygame.font.Font(None, 40)

    def Run(self):
        self.finished = False

        while not self.finished:
            #Handle input
            self.HandleInput()

            #Draw screen
            self.Draw()

            self.HandleDifficulty()

            self.clock.tick(60)
        
        pygame.quit()
        return True

    def HandleInput(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif not self.running:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.__init__()

        if self.running:
            if pygame.key.get_pressed()[K_DOWN]:
                if self.carSpeed + CARSPEEDCHANGE < MAXCARSPEED:
                    if self.carSpeed < 0:
                        #Make it quicker to slow down movement, makes the game feel more responsive
                        self.carSpeed += 2 * CARSPEEDCHANGE
                    else:
                        self.carSpeed += CARSPEEDCHANGE
            if pygame.key.get_pressed()[K_UP]:
                if self.carSpeed - CARSPEEDCHANGE > -MAXCARSPEED:
                    if self.carSpeed > 0:
                        self.carSpeed -= 2 * CARSPEEDCHANGE
                    else:
                        self.carSpeed -= CARSPEEDCHANGE

            self.carPos = self.carPos[0], self.carPos[1] + self.carSpeed
            colour = self.screen.get_at((round(self.carPos[0]) + self.car.get_size()[0], round(self.carPos[1])))
            if (colour == WALLCOLOUR):
                #Handle lose here
                self.running = False

    def Draw(self):
        #clear screen
        self.screen.blit(self.background, (0,0))

        #Draw backbar for text
        pygame.draw.rect(self.screen, (200,200,100), Rect(0, 0, XSIZE, YSPACING))

        if self.running:
            self.MoveRoad()
        
        #Draw road
        pos = 0
        pygame.draw.polygon(self.screen, WALLCOLOUR, self.roadPoses + [TOPRIGHT, TOPLEFT])
        pygame.draw.polygon(self.screen, WALLCOLOUR, self.roadBotPoses + [BOTTOMRIGHT, BOTTOMLEFT])
        #while pos + 1 < len(self.roadPoses):
        #    pygame.draw.line(self.screen, (10,10,10), self.roadPoses[pos], self.roadPoses[pos + 1])
        #    bottom1 = (self.roadPoses[pos][0], self.roadPoses[pos][1] + ROADSIZE)
        #    bottom2 = (self.roadPoses[pos + 1][0], self.roadPoses[pos + 1][1] + ROADSIZE)
        #    pygame.draw.line(self.screen, (10,10,10), bottom1, bottom2)
        #    pos += 1

        #Draw centered on the middle of the car
        if (self.running):
            self.screen.blit(self.car, (self.carPos[0], self.carPos[1] - self.car.get_size()[1]/2))
        elif self.carAnimCount < 31:
            self.carAnimCount += 1
            if self.carAnimCount < 10:
                self.screen.blit(self.car, (self.carPos[0], self.carPos[1] - self.car.get_size()[1]/2))
            elif self.carAnimCount < 20:
                self.screen.blit(self.car2, (self.carPos[0], self.carPos[1] - self.car.get_size()[1]/2))
            elif self.carAnimCount < 30:
                self.screen.blit(self.car3, (self.carPos[0], self.carPos[1] - self.car.get_size()[1]/2))

        #Draw timer
        if (self.running):
            self.score = math.floor(pygame.time.get_ticks()/1000 - self.startTime)
        timeStr = "Score: " + str(self.score)
        timeTxt = self.font.render(timeStr, True, (10,10,10))
        self.screen.blit(timeTxt, (XSIZE - timeTxt.get_size()[0], 0))

        #Draw end message
        if (not self.running):
            endStr = "Game over! Press Space to restart"
            endTxt = self.font.render(endStr, True, (10,10,100))
            self.screen.blit(endTxt, (0, 0))
        
        if (self.score >= 60 and not self.running):
            wowStr = "Wow! Impressive!"
            wowTxt = self.font.render(wowStr, True, (255, 240, 0))
            self.screen.blit(wowTxt, (XSIZE - wowTxt.get_size()[0], YSMALLSPACING))

        #Refresh the screen
        pygame.display.flip()
    
    def MoveRoad(self):
        newLocation = False
        toRemove = []

        for i in range(0, len(self.roadPoses)):
            if (self.roadPoses[i][0] == ROADLEFTX):
                newLocation = True
            self.roadPoses[i] = (self.roadPoses[i][0] - self.speed, self.roadPoses[i][1])
            self.roadBotPoses[i] = (self.roadBotPoses[i][0] - self.speed, self.roadBotPoses[i][1])
            if i < len(self.roadPoses) - 1:
                if (self.roadPoses[i + 1][0] < 0):
                    #Make sure the next position is off screen before removing
                    toRemove.append(i)

        #Remove the points we flagged to remove
        for i in toRemove:
            self.roadPoses.remove(self.roadPoses[i])
            self.roadBotPoses.remove(self.roadBotPoses[i])

        if newLocation == True:
            moving = random.randint(0, self.changeChance)
            amount = random.randint (1, MOVEAMOUNT)
            if (moving == 0 and (self.roadPoses[len(self.roadPoses) - 1][1] - amount) > MINY):
                #Move up
                self.roadPoses.append((ROADLEFTX, self.roadPoses[len(self.roadPoses) - 1][1] - amount))
                self.roadBotPoses.append((ROADLEFTX, self.roadPoses[len(self.roadPoses) - 1][1] - amount + self.roadSize))

            elif (moving == self.changeChance and (self.roadPoses[len(self.roadPoses) - 1][1] + amount) < (YSIZE - self.roadSize - YSMALLSPACING)):
                #Move down
                self.roadPoses.append((ROADLEFTX, self.roadPoses[len(self.roadPoses) - 1][1] + amount))
                self.roadBotPoses.append((ROADLEFTX, self.roadPoses[len(self.roadPoses) - 1][1] + amount + self.roadSize))
            else:
                #Don't add an element, but set the last element so it's at the end of the playfield
                self.roadPoses[len(self.roadPoses) - 1] = (ROADLEFTX, self.roadPoses[len(self.roadPoses) - 1][1])
                self.roadBotPoses[len(self.roadBotPoses) - 1] = (ROADLEFTX, self.roadBotPoses[len(self.roadBotPoses) - 1][1])
    
    def HandleDifficulty(self):
        if self.score < 10:
            return
        elif self.score < 20:
            self.speed = 4
            self.roadSize = 150
        elif self.score < 30:
            self.speed = 5
            self.roadSize = 120
            self.changeChance = 5
        elif self.score < 40:
            self.speed = 6
            self.roadSize = 100
        elif self.score < 50:
            self.speed = 7
            self.changeChance = 2
        else:
            self.speed = 8

#Run the game
game = KeepingOn()
game.Run()