'''
FlabbyPird.py
@Klaus
26.04.2022
'''

from email.charset import Charset
from locale import CHAR_MAX
from multiprocessing.sharedctypes import Value
from turtle import onclick
import pygame
from pygame.locals import *
import pygame_menu 
from sys import *
import random
import time
import sqlite3, sys
import functools
import operator

# Variables ====================


fps = 24
Width = 450
Height = 600

partikel = 10
brickspeed = 8
downspeed = 4
borderheight = Height - partikel*2.5



BLACK  = (0,0,0)
YELLOW = (255,255,0)
RED = (205,51,51)
GREEN = (0,128,0)

bricks = []



# Walking Bricks ================
# =============================================

class Bricks():
    def __init__(self, where, colour, left, top, width, height, speed):
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top 
        self.bottomtop = 0
        self.width = width
        self.height = height
        self.bottomheight = 0
        self.speed = speed
        self.gapHeight = Height/4
        self.gaplocker = random.randint(Height*0.3, Height*0.6)

    #====TWO DIFFERENT BRICKS WITHOUT GAP
    #===============================================

    def drawBrick (self):
        self.top = 0
        self.bodytop=pygame.draw.rect(self.where, self.colour, [self.left, self.top, self.width, self.height])
        self.bottomtop = self.height + self.gapHeight
        self.bottomheight = borderheight - self.bottomtop
        self.bodybottom=pygame.draw.rect(self.where, self.colour, [self.left, self.bottomtop, self.width, self.bottomheight])  

    def walk(self):        
        self.left -= self.speed

    def lvlUp(self):
        self.speed *= 1.2


# jumpinPird =======================
# =====================================================

class Pird():
    def __init__(self, where, colour, left, top, width, height, speed):
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.speed = speed
        self.jumpVar = -16
        self.player = ""
        self.counter = 0


    def drawPird(self):
        self.body=pygame.draw.ellipse(self.where, self.colour, [self.left, self.top, self.width, self.height])

    def fallDown(self):
        if self.top < Height:
            self.top += self.speed
            self.speed += 1.1


    def jumpUp(self):
        # stupid Jump
        # ======================
        #self.top -= self.speed*10

        # dynamic Jump
        # ========================
        if self.jumpVar == -16:
            self.jumpVar = 15

        if self.jumpVar >= -15:
            n = 1
            if self.jumpVar < 0:
                n = -1
            self.top -= (self.jumpVar**2.1)*0.17*n

        self.speed = downspeed

class Bottom():
    def __init__(self, where, colour, left, top, width, height):
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top 
        self.width = width
        self.height = height

    def draw(self):
        self.body=pygame.draw.rect(self.where, self.colour, [self.left, self.top, self.width, self.height])


# ======================================
# M A I N ==============================
# ======================================

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([Width, Height])      
pygame.display.set_caption("FlabbyPird")

border              =    Bottom(screen, GREEN, 0, borderheight, Width, partikel*2.5)
pird                =    Pird(screen,RED, Width*0.3, Height/2-partikel*2, partikel*4, partikel*3, downspeed)
topBrickHeight      =    random.randint(Height*0.3, Height*0.6)
startBrick          =    Bricks(screen, YELLOW , Width*2, 0, partikel*2, Height*0.4, brickspeed)
startBrick.height   =    topBrickHeight

bricks = []
bricks.append(startBrick)



# M A I N _ M E N U 
# ========================================= 

def mainManue():
    menu = pygame_menu.Menu('Flabby Pird', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.button('Play', start_the_game)
    menu.add.button('Score', scoreboard)       
    menu.add.button('Quit', pygame_menu.events.EXIT)       
    menu.mainloop(screen)   
    pygame.display.flip()
    clock.tick(fps)   
    

# S C O R E _ D B _ M A N A G E M E N T
# ==================================

def dbInput():
    try:
        db = sqlite3.connect("flabbyPird.db")
        cursor = db.cursor()
        print(pird.player)
        sql = "UPDATE score SET name = {0}, Score = {1} WHERE Score <= {1}",format(pird.player, str(pird.counter))
        print(sql)
        cursor.execute(sql)
        db.commit()   
        
    except: 
        print("Fehler beim INSERT - Datensatz wurde nicht gespeichert !")
        print("Unexpected error:", sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2] )  
    finally:
        db.close()


def dbOutput(lvl):
    try:
        db = sqlite3.connect("flabbyPird.db")
        cursor = db.cursor()
        sql = "SELECT * FROM score WHERE rowid = {0};".format(lvl)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        
        for e in result:
                output = e[0] + ' : ' + str(e[1])
                print(output)
        return output 
    except: 
        print("Fehler beim SELECT - Datensatz konnte nicht gelesen werden !")
        print("Unexpected error:", sys.exc_info()[1])  
    finally:
        db.close()

def dbSearch(count):
    try:
        db = sqlite3.connect("flabbyPird.db")
        cursor = db.cursor()
        # Searching for the position which is lower than players counter
        sql = "SELECT rowid FROM score WHERE Score <= {0};".format(count)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        db.commit()
        print(result) 
    except: 
        print("Fehler beim SELECT - Datensatz konnte nicht gelesen werden !")
        print("Unexpected error:", sys.exc_info()[1])  
    finally:
        db.close()




def getName(name):
    pird.player = name



# S C O R E _ M E N U
# =================================

def score(daCounter):
        menu = pygame_menu.Menu('Flabby Pird', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
        menu.add.text_input('Name: ', default='PLR', onchange=getName, maxchar=3)
        menu.add.label(daCounter)
        menu.add.button('Save', dbInput)
        menu.add.button('MAIN', mainManue)
        menu.mainloop(screen)   
        pygame.display.flip()
        clock.tick(fps)  
        
        

    
# S C O R E B O A R D
# ==========================================

def scoreboard():
    menu = pygame_menu.Menu('Flabby Pird', 400, 300, theme=pygame_menu.themes.THEME_SOLARIZED)
    menu.add.label(dbOutput(1))
    menu.add.label(dbOutput(2))
    menu.add.label(dbOutput(3))
    menu.add.button('Menu', start_the_game)
    menu.mainloop(screen)   
    pygame.display.flip()
    clock.tick(fps)    


# M A I N _ G A M E
# =================================================

def start_the_game():
    pird.counter = 0
    go = "j"
    while go == "j":
        screen.fill(BLACK)
        # ====== suicide pird
        border.draw()
        pird.drawPird()
        pird.fallDown()        
        # ============================
        # ====== the walking bricks
        for i in bricks:
            i.drawBrick()
            i.walk()
            if i.left <= Width*0.4 and i.left >= Width*0.39:       
                pird.counter += 1     
                topBrickHeight = random.randint(Height*0.2, Height*0.8)
                bricks.append(Bricks(screen, YELLOW, Width + partikel , 0, partikel*2, startBrick.height, brickspeed))
                bricks[pird.counter].height = topBrickHeight

            # Prepare To Die 
            #================================
            if i.bodytop.colliderect(pird.body) or i.bodybottom.colliderect(pird.body) or border.body.colliderect(pird.body):
                #time.sleep(3)
                dbSearch(pird.counter)
                score(pird.counter)
            # ==============================

        # ===========================

        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                go = "n"

            # jumpin`OutOfDeath ==============
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pird.jumpUp()

        my_font = pygame.font.Font(None, 50)
        surface = my_font.render(str(pird.counter), True, (255,255,255))
        text_rect = surface.get_rect()
        text_rect.center = (Width*0.75, Height * 0.15)
        screen.blit(surface, text_rect)

        pygame.display.flip()
        clock.tick(fps)




# R U N _ M A I N
# ===================================

mainManue()
