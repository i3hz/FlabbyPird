'''
FlabbyPird.py
@Klaus
26.04.2022
'''

import sqlite3, sys
import random
import pygame
import pygame_menu

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
        self.bodytop : pygame.surface
        self.bodybottom : pygame.surface


    def drawBrick (self):
        self.top = 0
        self.bodytop=pygame.draw.rect(self.where, self.colour, [self.left, self.top, self.width, self.height])
        self.bottomtop = self.height + self.gapHeight
        self.bottomheight = borderheight - self.bottomtop
        self.bodybottom=pygame.draw.rect(self.where, self.colour, [self.left, self.bottomtop, self.width, self.bottomheight])  

    def walk(self):
        self.left -= self.speed

    # not included jet
    # ========================
    def lvlUp(self):
        self.speed *= 1.2
    # ========================


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
        self.body : pygame.Surface

    def drawPird(self):
        self.body=pygame.draw.ellipse(self.where, self.colour, [self.left, self.top, self.width, self.height])

    # fallin` down faster and faster
    # ===================================
    def fallDown(self):
        if self.top < Height:
            self.top += self.speed
            self.speed += 1.1


    def jumpUp(self):
        if self.jumpVar == -16:
            self.jumpVar = 15

        if self.jumpVar >= -15:
            num = 1
            if self.jumpVar < 0:
                num = -1
            self.top -= (self.jumpVar**2.1)*0.17*num
        self.speed = downspeed


class Bottom():
    def __init__(self, where, colour, left, top, width, height):
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.body : pygame.surface

    def draw(self):
        self.body=pygame.draw.rect(self.where,
                                   self.colour,
                                  [self.left, self.top, self.width, self.height])


# ======================================
# M A I N ==============================
# ======================================

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([Width, Height])      
pygame.display.set_caption("FlabbyPird")

# objects
# =========================

border = Bottom(screen, GREEN, 0, borderheight, Width, partikel*2.5)
pird = Pird(screen,RED, Width*0.3, Height/2-partikel*2, partikel*4, partikel*3, downspeed)
topBrickHeight = random.randint(Height*0.3, Height*0.6)
startBrick = Bricks(screen, YELLOW , Width*2, 0, partikel*2, Height*0.4, brickspeed)
startBrick.height = topBrickHeight

# M E N U
# =========================================

class Menue():
    height = 400
    width = 320
    # M A I N _ M E N U
    # =========================================
    @staticmethod
    def mainManue():
        menu = pygame_menu.Menu('FLABBY PIRD',
                                 Menue.height,
                                 Menue.width,
                                 theme=pygame_menu.themes.THEME_SOLARIZED)
        menu.add.button('PLAY', start_the_game)
        menu.add.button('SCORE', Menue.scoreboard)
        menu.add.button('QUIT', pygame_menu.events.EXIT)
        menu.mainloop(screen)
        pygame.display.flip()
        clock.tick(fps)

    # S C O R E _ M E N U
    # =================================
    @staticmethod
    def get_name(name):
        pird.player = name.upper()

    @staticmethod
    def score(daCounter):
        menu = pygame_menu.Menu('SCORE', Menue.height, Menue.width,
                                 theme=pygame_menu.themes.THEME_SOLARIZED)
        pird.player = menu.add.text_input('Name: ',
                                           default='PLR',
                                           onchange=Menue.get_name ,
                                           maxchar=3, ).get_value().upper()
        menu.add.label(daCounter)
        menu.add.button('SAVE', DB.dbInput)
        menu.add.button('MENU', Menue.mainManue)
        menu.mainloop(screen)
        pygame.display.flip()
        clock.tick(fps)

    # S C O R E B O A R D
    # ==========================================
    @staticmethod
    def scoreboard():
        menu = pygame_menu.Menu('SCOREBOARD',Menue.height,Menue.width,
                                theme=pygame_menu.themes.THEME_SOLARIZED)
        menu.add.label(DB.dbOutput(0))
        menu.add.label(DB.dbOutput(1))
        menu.add.label(DB.dbOutput(2))
        menu.add.button('MENU', Menue.mainManue)
        menu.add.button('RESET SCOREBOARD', DB.dbRefresh)
        menu.mainloop(screen)
        pygame.display.flip()
        clock.tick(fps)

# S C O R E _ D B _ M A N A G E M E N T
# =============================================
class DB():
    @staticmethod
    def dbRefresh():
        try:
            database = sqlite3.connect("flabbyPird.db")
            cursor = database.cursor()
            delete = "DELETE FROM score"
            cursor.execute(delete)
            database.commit()
            print("DELETE FINISH")
            insert = "INSERT INTO score(name, Score) VALUES ('---', 0); "
            for i in range(3):
                cursor.execute(insert)
            database.commit()
            print("RESET COMPLETE")
            Menue.scoreboard()
        except: 
            print("Fehler beim Reset - Datensatz wurde nicht reseted !")
            print("Unexpected error:", sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2] )
        finally:
            database.close()

    @staticmethod
    def dbInput():
        try:
            database = sqlite3.connect("flabbyPird.db")
            cursor = database.cursor()
            name = str(pird.player)
            sco = str(pird.counter)
            sql = f"INSERT INTO score(name, Score) VALUES ('{name}', {sco})"
            cursor.execute(sql)
            database.commit()
            print("FINISH")
            Menue.scoreboard()
        except: 
            print("Fehler beim INSERT - Datensatz wurde nicht gespeichert !")
            print("Unexpected error:", sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2] )  
        finally:
            database.close()
    @staticmethod
    def dbOutput(lvl):
        try:
            database = sqlite3.connect("flabbyPird.db")
            cursor = database.cursor()
            sql = "SELECT * FROM score ORDER BY Score DESC;"
            cursor.execute(sql)
            catch = cursor.fetchall()
            zeile = catch[lvl]
            name = str(zeile[0])
            count = str(zeile[1])
            output = name + ' : ' + count
            # print(output)
            database.commit()
            return output
        except: 
            print("Fehler beim SELECT - Datensatz konnte nicht gelesen werden !")
            print("Unexpected error:", sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2] )  
        finally:
            database.close()
    @staticmethod
    def find_smallest_counter():
        min_list = []
        try:
            database = sqlite3.connect("flabbyPird.db")
            cursor = database.cursor()
            #sql = "SELECT MIN(Score) FROM score WHERE score < (SELECT Score FROM score ORDER BY Score DESC LIMIT 3);"
            sql = "SELECT Score FROM score ORDER BY Score DESC LIMIT 3;"
            cursor.execute(sql)
            #catch = cursor.fetchone()
            catch = cursor.fetchall()
            database.commit()
            
            sol = min([x[0] for x in catch])
            print(sol)
            return sol
        except: 
            print("Fehler beim Search - Datensatz konnte nicht gelesen werden !")
            print("Unexpected error:", sys.exc_info()[0],sys.exc_info()[1],sys.exc_info()[2] )  
        finally:
            database.close()

# DEFAULT SETTINGS
# ============================================
def default():
    # DEFAULT SETTINGS FOR PIRD
    # =================================
    pird.left = Width*0.3
    pird.top = Height/2-partikel*2
    pird.width = partikel*4
    pird.height = partikel*3
    pird.speed = downspeed
    pird.jumpVar = -16
    pird.player = ""

    # DEFAULT SETTINGS FOR BRICKS
    # ========================================
    startBrick.left = Width*2
    startBrick.top = 0
    startBrick.bottomtop = 0
    startBrick.width = partikel*2
    startBrick.height = Height*0.4
    startBrick.bottomheight = 0
    startBrick.speed = brickspeed
    startBrick.gapHeight = Height/4
    startBrick.gaplocker = random.randint(Height*0.3, Height*0.6)
    #print("DEFAUL-VALUES SETTED")
# ============================================

# SHOW SCORE:
def showScore():
    my_font = pygame.font.Font(None, 50)
    surface = my_font.render(str(pird.counter), True, (255,255,255))
    text_rect = surface.get_rect()
    text_rect.center = (Width*0.75, Height * 0.15)
    screen.blit(surface, text_rect)


# M A I N _ G A M E
# =================================================
def start_the_game():
    smalles_counter = int(DB.find_smallest_counter())
    pird.counter = 0
    bricks = []
    bricks.append(startBrick)
    go_game = "j"
    while go_game == "j":
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
                bricks.append(Bricks(screen,
                                     YELLOW,
                                     Width + partikel , 0, partikel*2,
                                     startBrick.height, brickspeed))
                bricks[pird.counter].height = topBrickHeight

            # COLLISSION DETECTION
            #================================
            if i.bodytop.colliderect(pird.body) or i.bodybottom.colliderect(pird.body) or border.body.colliderect(pird.body):
                default()
                if pird.counter > smalles_counter:
                    Menue.score(pird.counter)
                go_game = "n"

        # QUIT GAME
        # ===================================
        for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                go_game = "n"

            # jumpin`OutOfDeath ==============
            # ===================================
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pird.jumpUp()

        showScore()
        pygame.display.flip()
        clock.tick(fps)

# R U N _ M A I N
# ===================================
Menue.mainManue()
