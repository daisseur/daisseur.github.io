from snake import Snake
import pygame
import keyboard
from time import sleep
from random import randint

class Game:
    def __init__(self, width_height=(50, 50,), start_pos: tuple = None, cell=10):
        self.width, self.height = width_height
        self.start_pos = start_pos if start_pos else (round(self.width/2), round(self.height/2))
        self.cell = cell
        self.bg = (0, 0, 0,)
        self.__base_map = [[self.bg for i in range(self.height)] for i in range(50)]
        self.__map = [[self.bg for i in range(self.height)] for i in range(50)]
        self.__snake = Snake(self.start_pos)
        self.__snake.add_part()

    def spawn_apple(self):
        x = randint(1, self.height-1)
        y = randint(1, self.width-1)
        if self.__map[x][y] == (0, 0, 0,):
            self.__map[x][y] = (199, 55, 47,)

    def reload_map(self):
        for i_line in range(len(self.__map)):
            for i_color in range(len(self.__map[i_line])):
                if self.__map[i_line][i_color] != (199, 55, 47,):
                    self.__map[i_line][i_color] = (0, 0, 0,)

    def reset_map(self):
        self.__map = [[self.bg for i in range(self.height)] for i in range(50)]


    def show(self, first=False):
        pygame.init()
        self.px_width = self.width * self.cell
        self.px_height = self.height * self.cell
        screen = pygame.display.set_mode((self.px_width, self.px_height))

        cell_surf = pygame.Surface((self.cell, self.cell))
        for y, row in enumerate(self.__map):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.cell, y * self.cell, self.cell, self.cell)
                cell_surf.fill(cell)
                screen.blit(cell_surf, rect)
        if first:
            pygame.display.flip()
        else:
            pygame.display.update()

        return screen

    def self_collision(self):
        if self.__snake.get_pos() in self.__snake.parts_xy:
            return True
        else:
            return False

    def collision(self):
        print(self.__snake.get_pos())
        if self.__snake.y in [0, self.width]:
            # self.__snake.downgrade()
            return [True, "y"]
        elif self.__snake.x in [0, self.height]:
            # self.__snake.downgrade()
            return [True, "x"]
        else:
            return False

    def eat_apple(self):
        if self.__map[self.__snake.y][self.__snake.x] == (199, 55, 47):
            print("EATED")
            self.__snake.add_part()

    def set_all_part(self):
        for part in self.__snake.parts_xy:
            # print("part=", part)
            self.__map[part[1]][part[0]] = self.__snake.tail_color

    def game_over(self):
        """Je l'ai pas fait moi-même flm"""
        # Le fond
        screen = pygame.display.set_mode((self.px_width, self.px_height))
        screen.fill((255, 0, 0))
        # La police
        pol_go = pygame.font.SysFont("Perpetua Titling MT", 110)
        # Les textes
        txt_go = pol_go.render("GAME OVER", True, (255, 255, 255))
        # Les positions
        pos_go = txt_go.get_rect()
        pos_go.centerx = screen.get_rect().centerx

        # On colle sur la fenêtre
        screen.blit(txt_go, pos_go)
        pygame.display.update()

    def play(self):
        self.show(True)
        compteur = 0
        while True:
            self.reload_map()
            self.__map[self.__snake.y][self.__snake.x] = self.__snake.head_color
            self.set_all_part()
            self.show()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    print("quit")
                    quit()

            keys = pygame.key.get_pressed()
            sleep(0.1)
            self.__map[self.__snake.y][self.__snake.x] = self.bg
            if keys[pygame.K_z]:
                self.__snake.move_up()
            elif keys[pygame.K_s]:
                self.__snake.move_down()
            elif keys[pygame.K_d]:
                self.__snake.move_right()
            elif keys[pygame.K_q]:
                self.__snake.move_left()
            else:
                self.__snake.move()
            if self.collision():
                print("collision")
                for co in reversed(self.__snake.lasts_xy):
                    print(co, end='')
                    if co != self.__snake.get_pos():
                        self.__snake.x, self.__snake.y = co
                        break
                # self.__snake.add_part()
                print()
            if self.self_collision():
                self.game_over()
                print("GAME OVER")
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            print("quit")
                            return False
            self.eat_apple()
            compteur += 1
            if compteur == 10:
                compteur = 0
                self.spawn_apple()


if __name__ == "__main__":
    while True:
        Game(cell=20).play()