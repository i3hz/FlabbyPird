'''
FlabbyPird.py
@Klaus
26.04.2022
'''

import sqlite3
from sqlite3 import OperationalError
import random
import pygame
import pygame_menu

# Variables ====================
FPS = 24
WIDTH = 450
HEIGHT = 600

PARTIKEL = 10
BRICK_SPEED = 8
DOWN_SPEED = 4
BORDER_HEIGHT = HEIGHT - PARTIKEL*2.5

BLACK  = (0,0,0)
YELLOW = (255,255,0)
RED = (205,51,51)
GREEN = (0,128,0)

# Walking Bricks ================
# =============================================

class Bricks():
    """Build walking bricks with gaps to fly throug"""
    def __init__(self, where, colour, left, top, width, height, speed):
        """
        Args:
            where (pygame_surface): on which surface is the brick drawn
            colour (tupel): (255,255,0)
            left (double): x-position
            top (double): y-position
            width (int): object-width
            height (int): object-height
            speed (int): motion
        """
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top
        self.bottomtop = 0
        self.width = width
        self.height = height
        self.bottomheight = 0
        self.speed = speed
        self.gap_height = HEIGHT/4
        # gab position between bricks
        self.gaplocker = random.randint(HEIGHT*0.3, HEIGHT*0.6)
        #empty objects are filled in draw_bricks-method
        self.bodytop : pygame.surface
        self.bodybottom : pygame.surface


    def draw_brick(self):
        """Displays two bricks with gaps on different positions"""
        self.top = 0
        self.bodytop=pygame.draw.rect(self.where, self.colour,
                                     [self.left, self.top, self.width, self.height])
        self.bottomtop = self.height + self.gap_height
        self.bottomheight = BORDER_HEIGHT - self.bottomtop
        self.bodybottom=pygame.draw.rect(self.where, self.colour,
                                        [self.left, self.bottomtop, self.width, self.bottomheight])

    def walk(self):
        """ change position of bricks"""
        self.left -= self.speed


# jumpinPird =======================
# =====================================================

class Pird():
    """Players current figure"""
    def __init__(self, where, colour, left, top, width, height, speed):
        """
        Args:
            where (pygame_surface): on which surface is the pird drawn
            colour (tupel): (205,51,51)
            left (double): x-position
            top (double): y-position
            width (int): object-width
            height (int): object-height
            speed (int): motion
        """
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.speed = speed
        self.jump_var = -16
        self.player = ""
        self.counter = 0
        self.body : pygame.Surface

    def draw_pird(self):
        """Displays pird"""
        self.body=pygame.draw.ellipse(self.where, self.colour,
                                     [self.left, self.top, self.width, self.height])

    # fallin` down faster and faster
    # ===================================
    def fall_down(self):
        """automatic falldown"""
        if self.top < HEIGHT:
            self.top += self.speed
            self.speed += 1.1


    def jump_up(self):
        """Dynamic jump for pird"""
        if self.jump_var == -16:
            self.jump_var = 15

        if self.jump_var >= -15:
            num = 1
            if self.jump_var < 0:
                num = -1
            self.top -= (self.jump_var**2.1)*0.17*num
        self.speed = DOWN_SPEED


class Bottom():
    """Create bottom-ground"""
    def __init__(self, where, colour, left, top, width, height):
        """
        Args:
            where (pygame_surface): on which surface is the bottom drawn
            colour (tupel): (205,51,51)
            left (double): x-position
            top (double): y-position
            width (int): object-width
            height (int): object-height
        """
        self.where = where
        self.colour = colour
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.body : pygame.surface

    def draw(self):
        """ Displays bottomground"""
        self.body=pygame.draw.rect(self.where,
                                   self.colour,
                                  [self.left, self.top, self.width, self.height])


# ======================================
# pygame initialisation ================
# ======================================

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("FlabbyPird")

# objects for futher operations based on delevoped classes above
# =========================
border = Bottom(screen, GREEN, 0, BORDER_HEIGHT, WIDTH, PARTIKEL*2.5)
pird = Pird(screen,RED, WIDTH*0.3, HEIGHT/2-PARTIKEL*2, PARTIKEL*4, PARTIKEL*3, DOWN_SPEED)
topBrickHeight = random.randint(HEIGHT*0.3, HEIGHT*0.6)
startBrick = Bricks(screen, YELLOW , WIDTH*2, 0, PARTIKEL*2, HEIGHT*0.4, BRICK_SPEED)
startBrick.height = topBrickHeight

# U T I L I T Y  C L A S S E S
# ===================================================================
# M E N U
# =========================================

class Menue():
    """Map for menu coordination"""
    height = 400
    width = 320
    # M A I N _ M E N U
    # =========================================
    @staticmethod
    def main_manue():
        """ Coordination to current game, Scoreboard or quitting the game"""
        menu = pygame_menu.Menu('FLABBY PIRD',
                                 Menue.height,
                                 Menue.width,
                                 theme=pygame_menu.themes.THEME_SOLARIZED)
        menu.add.button('PLAY', start_the_game)
        menu.add.button('SCORE', Menue.scoreboard)
        menu.add.button('QUIT', pygame_menu.events.EXIT)
        menu.mainloop(screen)
        pygame.display.flip()
        clock.tick(FPS)

    # S C O R E _ M E N U
    # =================================
    @staticmethod
    def get_name(name):
        """Allocate input name to players name in upper case
        Args:
            name (string): player´s name
        """
        pird.player = name.upper()

    @staticmethod
    def score(da_counter):
        """Is shown when player´s score is high enough for saving in database
        Args:
            da_counter (int_): current score
        """
        menu = pygame_menu.Menu('SCORE', Menue.height, Menue.width,
                                 theme=pygame_menu.themes.THEME_SOLARIZED)
        pird.player = menu.add.text_input('Name: ',
                                           default='PLR',
                                           onchange=Menue.get_name ,
                                           maxchar=3, ).get_value().upper()
        menu.add.label(da_counter)
        # call the db_input function
        menu.add.button('SAVE', DB.db_input)
        # back to main menu
        menu.add.button('MENU', Menue.main_manue)
        menu.mainloop(screen)
        pygame.display.flip()
        clock.tick(FPS)

    # S C O R E B O A R D
    # ==========================================
    @staticmethod
    def scoreboard():
        """Displays saved Scores from Database"""
        menu = pygame_menu.Menu('SCOREBOARD',Menue.height,Menue.width,
                                theme=pygame_menu.themes.THEME_SOLARIZED)
        menu.add.label(DB.db_output(0))
        menu.add.label(DB.db_output(1))
        menu.add.label(DB.db_output(2))
        menu.add.button('MENU', Menue.main_manue)
        menu.add.button('RESET SCOREBOARD', DB.db_refresh)
        menu.mainloop(screen)
        pygame.display.flip()
        clock.tick(FPS)

# S C O R E _ D B _ M A N A G E M E N T
# =============================================
class DB():
    """Database management
       The database will be opened in each function and will be closed no matter if
       the actions was successfull"""

    @staticmethod
    def db_refresh():
        """Reset the whole database and insert three emtpy names and scores.
           This displays a clean database and provides base-scores for comparision"""
        try:
            database = sqlite3.connect("flabbyPird.db")
            cursor = database.cursor()
            delete = "DELETE FROM score"
            cursor.execute(delete)
            database.commit()
            print("DELETE FINISH")
            insert = "INSERT INTO score(name, Score) VALUES ('---', 0),('---', 0),('---', 0);"
            cursor.execute(insert)
            database.commit()
            print("RESET COMPLETE")
            Menue.scoreboard()
        except OperationalError as exc:
            print("Fehler beim Reset - Datensatz wurde nicht reseted !")
            print(f"Unexpected error: {exc}")
            database.close()

    @staticmethod
    def db_input():
        """Append the current player score in addition to his acronym"""
        try:
            database = sqlite3.connect("flabbyPird.db")
            cursor = database.cursor()
            name = str(pird.player)
            sco = str(pird.counter)
            sql = f"INSERT INTO score(name, Score) VALUES ('{name}', {sco});"
            cursor.execute(sql)
            database.commit()
            Menue.scoreboard()
        except OperationalError as exc:
            print("Fehler beim INSERT - Datensatz wurde nicht gespeichert !")
            print(f"Unexpected error: {exc}")
        finally:
            database.close()

    @staticmethod
    def db_output(lvl):
        """read names and scores from database

        Args:
            lvl (int): rowid

        Returns:
            string: scoreboard content
        """
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
            database.commit()
            return output
        except OperationalError as exc:
            print("Fehler beim SELECT - Datensatz konnte nicht gelesen werden !")
            print(f"Unexpected error: {exc}")
        finally:
            database.close()

    @staticmethod
    def find_smallest_counter():
        """Find the smallest score out of the three highest scores from database for comparing
            with the current player Score

        Returns:
            int: smalles score
        """
        try:
            database = sqlite3.connect("flabbyPird.db")
            cursor = database.cursor()
            sql = "SELECT MIN(Score) FROM (SELECT Score FROM score ORDER BY Score DESC LIMIT 3);"
            cursor.execute(sql)
            sol = cursor.fetchone()[0]
            database.commit()
            return sol
        except OperationalError as exc:
            print("Fehler beim Search - Datensatz konnte nicht gelesen werden !")
            print(f"Unexpected error: {exc}")
        finally:
            database.close()

# ===================================================================

# DEFAULT SETTINGS
# =================================================
def default():
    """ Default positions for pird and brickwalk, wich were called
        every time a new game starts """
    # pird
    pird.left = WIDTH*0.3
    pird.top = HEIGHT/2-PARTIKEL*2
    pird.width = PARTIKEL*4
    pird.height = PARTIKEL*3
    pird.speed = DOWN_SPEED
    pird.jump_var = -16
    pird.player = ""

    # bricks
    startBrick.left = WIDTH*2
    startBrick.top = 0
    startBrick.bottomtop = 0
    startBrick.width = PARTIKEL*2
    startBrick.height = HEIGHT*0.4
    startBrick.bottomheight = 0
    startBrick.speed = BRICK_SPEED
    startBrick.gap_height = HEIGHT/4
    startBrick.gaplocker = random.randint(HEIGHT*0.3, HEIGHT*0.6)
# =================================================


# SHOW SCORE:
def show_score():
    """ Draw Score on gamewindow """
    my_font = pygame.font.Font(None, 50)
    surface = my_font.render(str(pird.counter), True, (255,255,255))
    text_rect = surface.get_rect()
    text_rect.center = (WIDTH*0.75, HEIGHT * 0.15)
    screen.blit(surface, text_rect)


# M A I N _ G A M E
# =================================================
def start_the_game():
    """ Mainloop for indeed game, collision detection and controlling """
    smallest_counter = int(DB.find_smallest_counter())
    pird.counter = 0
    bricks = []
    bricks.append(startBrick)
    go_game = "j"
    while go_game == "j":
        screen.fill(BLACK)
        # ====== suicide pird
        border.draw()
        pird.draw_pird()
        pird.fall_down()
        # ============================
        # ====== the walking bricks
        for brick in list(bricks):
            brick.draw_brick()
            brick.walk()
            if brick.left <= WIDTH*0.4 and brick.left >= WIDTH*0.39:
                pird.counter += 1
                top_brick_height = random.randint(HEIGHT*0.2, HEIGHT*0.8)
                #create new Bricks in in bricklist
                bricks.append(Bricks(screen,
                                     YELLOW,
                                     WIDTH + PARTIKEL , 0, PARTIKEL*2,
                                     startBrick.height, BRICK_SPEED))
                bricks[pird.counter].height = top_brick_height

            # COLLISSION DETECTION
            #================================
            if (brick.bodytop.colliderect(pird.body) or
                brick.bodybottom.colliderect(pird.body) or border.body.colliderect(pird.body)):
                default()
                # evaluate if reached score is high enough for saving player`s name in database
                if pird.counter > smallest_counter:
                    Menue.score(pird.counter)
                go_game = "n"

        # QUIT GAME
        # ===================================
        for event in pygame.event.get():
            if (event.type==pygame.QUIT or
               (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                go_game = "n"

            # jumpin`OutOfDeath / Controlling ==============
            # ===================================
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pird.jump_up()

        show_score()
        pygame.display.flip()
        clock.tick(FPS)

# R U N _ M A I N _ M E N U
# ===================================
Menue.main_manue()
