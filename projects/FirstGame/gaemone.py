import keyboard
from time import sleep
import time
from os import system as cmd
from os import get_terminal_size
from random import randint
import pygame

nocolor = "\033[0;0m"
colors = {
    'black': '0;',
    'red': '1;',
    'green': '2;',
    'yellow': '3;',
    'blue': '4;',
    'violet': '5;',
    'cyan': '6;',
    'grey': '7;',
    'white': '9;'}
effects = {
    'bold': '1m',
    'classic': '2m',
    'italic': '3m',
    'underline': '4m',
    'strike': '9m'}
highlights = {
    'False': '\033[3',
    'True': '\033[4'}

def print_color(*args, color='white', effect='classic', highlight='False', end=False) -> None:
    if end:
        print(highlights[highlight] + colors[color] + effects[effect] + ' '.join(str(arg) for arg in args) + nocolor, end='')
    else:
        print(highlights[highlight] + colors[color] + effects[effect] + ' '.join(str(arg) for arg in args) + nocolor)

class playterm:
    def __init__(self, points=1, speed=0.001, cell=10):
        self.cell = 10
        self.limit_color = (158, 3, 16,)
        self.bg = (0, 0, 0,)
        self.point_color = (255, 255, 255,)
        self.player_color = (255, 255, 0,)
        self.term_size = get_terminal_size()
        self.speed = speed
        self.map = [[self.bg for i in range(self.term_size.columns-2)] for i in range(50)]
        # set outlines
        self.map = [[self.limit_color for i in range(len(self.map[0]))]] + self.map
        self.map = self.map + [[self.limit_color for i in range(len(self.map[0]))]]
        for i in range(len(self.map)):
            self.map[i] = [self.limit_color] + self.map[i] + [self.limit_color]
        # print(self.map)
        self.points = []
        for n in range(points):
            point = [randint(2, len(self.map)-2), randint(2, len(self.map[1])-1)]
            while point in self.points:
                point = [randint(2, len(self.map)-1), randint(2, len(self.map[1])-1)]
            self.points.append(point)
            print(self.map[point[0]])
            self.map[point[0]][point[1]] = self.point_color
        self.map[2][1] = self.player_color
        self.location = [2, 1]
        self.short_time = []

    def up(self, location=[2, 1]):
        if location[0] != 1:
            self.map[location[0]][location[1]] = self.bg
            location[0] -= 1
            self.map[location[0]][location[1]] = self.player_color
            return location
        else:
            print("UP ERROR")
            return location

    def down(self, location=[2, 1]):
        if location[0] != len(self.map) -2:
            self.map[location[0]][location[1]] = self.bg
            location[0] += 1
            self.map[location[0]][location[1]] = self.player_color
            return location
        else:
            print("DOWN ERROR")
            return location

    def right(self, location=[2, 1]):
        if location[1] != len(self.map[location[0]]) -2:
            self.map[location[0]][location[1]] = self.bg
            location[1] += 1
            self.map[location[0]][location[1]] = self.player_color
            return location
        else:
            print("RIGHT ERROR")
            return location

    def left(self, location=[2, 1]):
        if location[1] != 1:
            self.map[location[0]][location[1]] = self.bg
            location[1] -= 1
            self.map[location[0]][location[1]] = self.player_color
            return location
        else:
            print("LEFT ERROR")
            return location

    def show_map(self, map, cell_size, first=False):
        pygame.init()
        width = len(map[0]) * cell_size
        height = len(map) * cell_size
        screen = pygame.display.set_mode((width, height))
        
        # Crée une surface rectangulaire pour chaque case de la carte
        cell_surf = pygame.Surface((cell_size, cell_size))
        for y, row in enumerate(map):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
                cell_surf.fill(cell)
                screen.blit(cell_surf, rect)
        if first:
            pygame.display.flip()
        else:
            pygame.display.update()

        return screen



    def show(self):
        screen = self.show_map(self.map, self.cell, first=True)
        print("press z, s, d or q\n")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                location = self.up(self.location)
            elif keys[pygame.K_s]:
                location = self.down(self.location)
            elif keys[pygame.K_d]:
                location = self.right(self.location)
            elif keys[pygame.K_q]:
                location = self.left(self.location)
            else:
                continue
            screen = self.show_map(self.map, self.cell, first=False)
            sleep(self.speed)
            if location in self.points:
                del self.points[self.points.index(location)]
                if len(self.points) == 0:
                    break


if __name__ == "__main__":
    speed = 0.1
    points = 1
    for level in range(1, 10):
        playterm(points=int(round(points)), speed=speed, cell=5).show()
        speed = speed/7 * 3
        print(speed)
        points = points*1.40
        print(points)
        sleep(1)