import sys
import pygame
from pygame.locals import *
from math import floor
import random

tile_size = 32
map_size = 16

'''initialisation of the window'''


def init_window():  # Generating the window
    pygame.init()
    pygame.display.set_mode((map_size * tile_size, map_size * tile_size))
    pygame.display.set_caption('Pacman')


'''Function with pygame method Surface, which draws the window'''


def draw_background(scr, img=None):  # Drawing the background
    if img:
        scr.blit(img, (0, 0))
    else:
        bg = pygame.Surface(scr.get_size())
        bg.fill((128, 128, 128))
        scr.blit(bg, (0, 0))


'''Common class, which is the origin for all object classes (Pacman, Ghosts, State objects)'''


class GameObject(
    pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.screen_rect = None
        self.x = 0
        self.y = 0
        self.tick = 0
        self.set_coord(x, y)

    def set_coord(self, x, y):  # setting coordinates to objects according to the map file
        self.x = x
        self.y = y
        self.screen_rect = Rect(floor(x) * tile_size, floor(y) * tile_size, tile_size, tile_size)

    def game_tick(self):  # Game time
        self.tick += 1

    def draw(self, scr):  # Pygame function, drawing all the objects
        scr.blit(self.image, (self.screen_rect.x, self.screen_rect.y))


'''This class refers to the common GameObject class, includes the information about moving of the ghost'''


class Ghost(GameObject):
    ghosts = []  # massiv of ghosts

    def __init__(self, x, y):
        GameObject.__init__(self, './resources/ghost.png', x, y)
        self.direction = 0
        self.velocity = 3.5 / 10.0

    @property
    def intellect(self):  # AI of "clever ghosts"
        x, y = int(self.x), int(self.y)
        if y == int(pacman.y):
            for X in range(x, 16):
                if isinstance(MAP.map[y][X], Wall):
                    break
                if X == int(pacman.x):  # Checking the pacman coord (ghost sees it) and makes a decision
                    return 1 if not EatBonus.eat_bonus \
                        else 3
            for X in reversed(range(x)):
                if isinstance(MAP.map[y][X], Wall):
                    break
                if X == int(pacman.x):
                    return 3 if not EatBonus.eat_bonus \
                        else 1
        if x == int(pacman.x):
            for Y in range(y, 16):
                if isinstance(MAP.map[Y][x], Wall):
                    break
                if Y == int(pacman.y):
                    return 2 if not EatBonus.eat_bonus \
                        else 4
            for Y in reversed(range(y)):
                if isinstance(MAP.map[Y][x], Wall):
                    break
                if Y == int(pacman.y):
                    return 4 if not EatBonus.eat_bonus \
                        else 2

    def game_tick(self):  # Movings of the ghosts with time
        super(Ghost, self).game_tick()

        if self.tick % 20 == 0 or self.direction == 0:  # direction: 1-moving right 2- up 3-left 4- down
            self.direction = random.randint(1, 4)

        decision = self.intellect
        if decision:  # clever ghosts move according to the def "Intellect and their initial "direction", when ghost meets the wall, it stopps"
            self.direction = decision

        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y):
                self.x += self.velocity
            if self.x >= map_size - 1:
                self.x = map_size - 1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)):
                self.y += self.velocity
            if self.y >= map_size - 1:
                self.y = map_size - 1
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
        if floor(pacman.x) == floor(self.x) and floor(pacman.y) == floor(
                self.y) and EatBonus.eat_bonus:  # Pacman eats ghosts
            Ghost.ghosts.remove(self)

            pacman.score += 2
        elif floor(pacman.x) == floor(self.x) and floor(pacman.y) == floor(self.y):
            print('You lose! Your score is ', str(pacman.score))
            exit()
        self.set_coord(self.x, self.y)


'''This type of ghost has no def Intellect, it has much in common with Ghost'''


class StupidGhost(GameObject):
    stupidghosts = []  # massiv of stupidghosts

    def __init__(self, x, y):
        GameObject.__init__(self, './resources/ghost.png', x, y)
        self.direction = 0
        self.velocity = 3.5 / 10.0

    def game_tick(self):  # The same structure as clever ghosts
        super(StupidGhost, self).game_tick()

        if self.tick % 20 == 0 or self.direction == 0:
            self.direction = random.randint(1, 4)

        if self.direction == 1:
            if not is_wall(floor(self.x + self.velocity), self.y):
                self.x += self.velocity
            if self.x >= map_size - 1:
                self.x = map_size - 1
                self.direction = random.randint(1, 4)
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)):
                self.y += self.velocity
            if self.y >= map_size - 1:
                self.y = map_size - 1
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
        if floor(pacman.x) == floor(self.x) and floor(pacman.y) == floor(self.y) and EatBonus.eat_bonus:
            StupidGhost.stupidghost.remove(self)

            pacman.score += 2
        elif floor(pacman.x) == floor(self.x) and floor(pacman.y) == floor(self.y):
            print('You lose! Your score is ', str(pacman.score))
            exit()
        self.set_coord(self.x, self.y)


'''In addition to GameObject, there is an information about moving and meeting of the pacman with bonuses'''


class Pacman(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, './resources/pacman.png', x, y)
        self.direction = 0
        self.velocity = 4.0 / 10.0
        self.score = 0

    def __get_direction(self):
        return self.__direction

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
            if self.x >= map_size - 1:
                self.x = map_size - 1
        elif self.direction == 2:
            if not is_wall(self.x, floor(self.y + self.velocity)):
                self.y += self.velocity
            if self.y >= map_size - 1:
                self.y = map_size - 1
        elif self.direction == 3:
            if not is_wall(floor(self.x - self.velocity), self.y):
                self.x -= self.velocity
            if self.x <= 0:
                self.x = 0
        elif self.direction == 4:
            if not is_wall(self.x, floor(self.y - self.velocity)):
                self.y -= self.velocity
            if self.y <= 0:
                self.y = 0

        self.set_coord(self.x, self.y)

        if isinstance(MAP.map[int(self.y)][int(self.x)], Food):  # checking meeting pacman with objects
            MAP.map[int(self.y)][int(self.x)] = None
            self.score += 1
            Food.num -= 1
            if Food.num == 0:
                print('WINNER Score:', str(pacman.score))  # When there is no food items on the map, the game is done
                exit()

        if isinstance(MAP.map[int(self.y)][int(self.x)], Bonus):
            MAP.map[int(self.y)][int(self.x)] = None
            pacman.velocity = 6.5 / 10.0
        if isinstance(MAP.map[int(self.y)][int(self.x)], EatBonus):
            MAP.map[int(self.y)][int(self.x)] = None
            EatBonus.eat_bonus = 1
        if isinstance(MAP.map[int(self.y)][int(self.x)], EatableWall) == True:
            MAP.map[int(self.y)][int(self.x)] = None
            if EatableWall.isfood == 1:
                MAP.map[-1].append(Food(self.x, self.y))
                Food.append(self.x, self.y)


def draw_ghosts(screen):
    for g in Ghost.ghosts:
        g.draw(screen)
    for g in StupidGhost.stupidghosts:
        g.draw(screen)


def tick_ghosts():
    for g in Ghost.ghosts:
        g.game_tick()
    for g in StupidGhost.stupidghosts:
        g.game_tick()


'''class of walls, that can be ruined by Pacman'''


class EatableWall(GameObject):
    isfood = 0

    def __init__(self, x, y):
        GameObject.__init__(self, './resources/wall.png', x, y)

    def game_tick(self):
        super(EatableWall, self).game_tick()


def create_eatable_walls():
    EatableWall.w = [EatableWall(1, 1)]


class Wall(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, './resources/wall.png', x, y)

    def game_tick(self):
        super(Wall, self).game_tick()


def create_walls():
    EatableWall.w = [EatableWall(1, 1)]


def draw_eatable_walls(screen):
    for w in EatableWall.w:
        GameObject.draw(w, screen)


def is_wall(x, y):  # checking the existance of the wall
    return isinstance(MAP.map[int(y)][int(x)], Wall)


def draw_walls(screen):
    for w in Wall.w:
        GameObject.draw(w, screen)


class Food(GameObject):
    num = 0

    def __init__(self, x, y):
        GameObject.__init__(self, './resources/food.png', x, y)


class Bonus(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, './resources/bonus.png', x, y)


'''Checking class, made only for simplification of using the meetings of pacman with bonuses in other defs'''


class EatBonus(GameObject):
    eat_bonus = None

    def __init__(self, x, y):
        GameObject.__init__(self, './resources/eat.png', x, y)


'''this class includes information about all objects of the map in 2-measured array'''


class Map:
    def __init__(self, filename):
        self.map = []
        f = open(filename, 'r')
        txt = f.readlines()
        f.close()
        for y in range((map_size)):
            self.map.append([])
            for x in range((map_size)):
                if '#' in txt[y][x]:
                    self.map[-1].append(Wall(x, y))  # Filling the map according to the symbols in file
                elif '.' in txt[y][x]:
                    self.map[-1].append(Food(x, y))
                    Food.num += 1
                elif txt[y][x] == "+":
                    self.map[-1].append(Bonus(x, y))
                elif txt[y][x] == "%":
                    self.map[-1].append(EatableWall(x, y))
                elif txt[y][x] == "*":
                    EatableWall.isfood = 1
                    self.map[-1].append(EatableWall(x, y))
                elif txt[y][x] == "&":
                    self.map[-1].append(EatBonus(x, y))
                elif txt[y][x] == "G":
                    Ghost.ghosts.append(Ghost(x, y))
                    self.map[-1].append(None)
                elif txt[y][x] == "S":
                    StupidGhost.stupidghosts.append(StupidGhost(x, y))
                    self.map[-1].append(None)
                else:
                    self.map[-1].append(None)

    def draw(self, screen):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x]:
                    self.map[y][x].draw(screen)  # draw, if smth is in that square x*y


def process_events(events, packman):  # Checking the user has clicked the key
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
    pacman = Pacman(13, 5)
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
