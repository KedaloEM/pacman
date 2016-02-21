import sys
import pygame
from pygame.locals import *
from math import floor
import random
tile_Size = 32
map_Size = 18


def init_window():   #Generating the window
    pygame.init()
    pygame.display.set_mode((map_Size * tile_Size, map_Size * tile_Size))
    pygame.display.set_caption('Pacman')


def draw_background(scr, img=None):
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.set_coord(x, y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * tile_Size, floor(y) * tile_Size, tile_Size, tile_Size )

    def game_tick(self):
        self.tick += 1

    def draw(self, scr):
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


class Ghost(GameObject):
    ghosts = []  #massiv of ghosts
    num = 4
    def __init__(self, x, y):
        GameObject.__init__(self, './resources/ghost.png', x, y)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def Intellect(self):
        x , y = int(self.x), int(self.y)
        if y == int(pacman.y):
            for X in range(x, 16):
                if isinstance(MAP.map[y][X], Wall): break
                if X == int(pacman.x):
                    return 1 if not EatBonus.eat_bonus else 3
            for X in reversed(range(x)):
                if isinstance(MAP.map[y][X], Wall): break
                if X == int(pacman.x):
                    return 3 if not EatBonus.eat_bonus else 1
        if x == int(pacman.x):
            for Y in range(y, 16):
                if isinstance(MAP.map[Y][x], Wall): break
                if Y == int(pacman.y):
                    return 2 if not EatBonus.eat_bonus else 4
            for Y in reversed(range(y)):
                if isinstance(MAP.map[Y][x], Wall): break
                if Y == int(pacman.y):
                    return 4 if not EatBonus.eat_bonus else 2

    def game_tick(self):
         super(Ghost, self).game_tick()

         if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

         decision = self.Intellect()
         if decision: self.direction = decision

         if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y):
                self.x += self.velocity
            if self.x >= map_Size-1:
                self.x = map_Size-1
                self.direction = random.randint(1, 4)
         elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)):
                self.y += self.velocity
            if self.y >= map_Size-1:
                self.y = map_Size-1
                self.direction = random.randint(1, 4)
         elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                    self.x = 0
                    self.direction = random.randint(1, 4)
         elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0
                self.direction = random.randint(1, 4)
         if floor(pacman.x) == floor(self.x) and floor(pacman.y) == floor(self.y)  and EatBonus.eat_bonus:
              Ghost.ghosts.remove(self)
         self.set_coord(self.x, self.y)


class Pacman(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, './resources/pacman.png', x, y)
        self.direction = 0
        self.velocity = 4.0 / 10.0

    def __get_direction(self):
        return self.__direction;
    def __set_direction(self, d):
        self.__direction = d
        if d == 1:
            self.image = pygame.image.load('./resources/pacman_right.png')
        elif d == 2:
            self.image = pygame.image.load('./resources/pacman_down.png')
        elif d == 3:
            self.image = pygame.image.load('./resources/pacman_left.png')
        elif d == 4:
            self.image = pygame.image.load('./resources/pacman_up.png')
        elif d != 0:
            raise ValueError("invalid direction detected")
    direction = property(__get_direction, __set_direction)

    def game_tick(self):
        super(Pacman, self).game_tick()
        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y):
                self.x += self.velocity
            if self.x >= map_Size-1:
                self.x = map_Size-1
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y+self.velocity)):
                self.y += self.velocity
            if self.y >= map_Size-1:
                self.y = map_Size-1
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y-self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.set_coord(self.x, self.y)

        if isinstance(MAP.map[int(self.y)][int(self.x)], Food):  # checking meeting pacman with objects
            MAP.map[int(self.y)][int(self.x)] = None
        if isinstance(MAP.map[int(self.y)][int(self.x)], Bonus):
            MAP.map[int(self.y)][int(self.x)] = None
            pacman.velocity = 10.0/10.0
        if isinstance(MAP.map[int(self.y)][int(self.x)], BadBonus):
            MAP.map[int(self.y)][int(self.x)] = None
            Ghost.num = 10
        if isinstance(MAP.map[int(self.y)][int(self.x)], EatBonus)  == True:
            MAP.map[int(self.y)][int(self.x)] = None
            EatBonus.eat_bonus = 1

def draw_ghosts(screen):
    for g in Ghost.ghosts:
        g.draw(screen)

def tick_ghosts():
    for g in Ghost.ghosts:
        g.game_tick()


class Food(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self,'./resources/food.png', x, y)




class Wall(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, './resources/wall.png', x, y)
    def game_tick(self):
        super(Wall, self).game_tick()

def create_walls(coords):
    Wall.w = [Wall(2,4)]

def is_wall(x, y):
    return isinstance(MAP.map[int(y)][int(x)], Wall)

def draw_walls(screen):
    for w in Wall.w:
        GameObject.draw(w,screen)

class Bonus(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self,'./resources/bonus.png', x, y)


class BadBonus(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self,'./resources/death.png', x, y)

class EatBonus(GameObject):
    eat_bonus = None
    def __init__(self, x, y):
        GameObject.__init__(self, './resources/eat.png', x, y)

class Map:
        def __init__(self, filename):
            self.map = []
            f=open(filename, 'r')
            txt = f.readlines()
            f.close()
            for y in range(len(txt)):
                self.map.append([])
                for x in range(len(txt[y])):
                    if '#' in txt[y][x]:
                        self.map[-1].append(Wall(x, y))  #Filling the map according to the symbols in file
                    elif '.' in txt[y][x]:
                        self.map[-1].append(Food(x, y))
                    elif txt[y][x] == "+":
                        self.map[-1].append(Bonus(x, y))
                    elif txt[y][x] == "-":
                        self.map[-1].append(BadBonus(x, y))
                    elif txt[y][x] == "&":
                        self.map[-1].append(EatBonus(x, y))
                    elif txt[y][x] == "G":
                        Ghost.ghosts.append(Ghost(x ,y))
                    else:
                        self.map[-1].append(None)
        def draw(self, screen):
            for y in range(len(self.map)):
                for x in range(len(self.map[y])):
                    if self.map[y][x]:
                       self.map[y][x].draw(screen) #draw, if smth is in that square x*y





def process_events(events, packman):
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                packman.direction = 3
            elif event.key == K_RIGHT:
                packman.direction = 1
            elif event.key == K_UP:
                packman.direction = 4
            elif event.key == K_DOWN:
                packman.direction = 2
            elif event.key == K_SPACE:
                packman.direction = 0


if __name__ == '__main__':
    init_window()

    global MAP
    MAP = Map('map.txt')
    pacman = Pacman(5, 5)
    background = pygame.image.load("./resources/background1.png")
    screen = pygame.display.get_surface()

    while 1:
        process_events(pygame.event.get(), pacman)
        pygame.time.delay(50)
        tick_ghosts()
        pacman.game_tick()
        draw_background(screen, background)
        pacman.draw(screen)
        draw_ghosts(screen)
        MAP.draw(screen)
        pygame.display.update()