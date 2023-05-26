import json
import numpy as np
import pygame
from time import sleep, perf_counter
from math import isnan
from os.path import exists
from ast import literal_eval
import sys
import signal

EMERGENCY_END = False
closable = True


def signal_handler(signal, frame):
    global EMERGENCY_END
    global closable
    EMERGENCY_END = True
    print("STOPPED")
    sleep(1)
    sys.exit()


def get_lifeId(array):
    lifeId = ''
    for y in range(array.shape[0]):
        for x in range(array.shape[1]):
            lifeId += str(array[y, x])
    return lifeId


def get_array(lifeId):
    lifeId = str(lifeId)
    for n in range(0, 51, 5):
        if n * n == len(lifeId):
            lst = []
            for i in range(n):
                lst.append([])
            index = 0
            for digit in lifeId:
                lst[index].append(int(digit))
                if len(lst[index]) == n:
                    index += 1
    array = np.array(lst)
    return array


def get_lists(lifeId):
    lifeId = str(lifeId)
    for n in range(0, 51, 5):
        if n * n == len(lifeId):
            lst = []
            for i in range(n):
                lst.append([])
            index = 0
            for digit in lifeId:
                lst[index].append(int(digit))
                if len(lst[index]) == n:
                    index += 1
    return lst


class LifeGame:
    def __init__(self, height=100, width=100, border=3, delay=1, cell_size=5, log=False):
        global EMERGENCY_END
        self.height, self.width, self.border, self.delay, self.cell_size, self.log = height, width, border, delay, cell_size, log
        self.reset()
        self.screen = None

        self.results = {}

    def reset(self):

        self.a = np.zeros((self.height, self.width), dtype=int)
        self.new_a = np.zeros((self.height, self.width), dtype=int)

    def set(self, lifeId, yx=(0, 0)):
        if yx == (0, 0):
            yx = (round(self.height / 2), round(self.width / 2))
        y, x = yx
        figure = get_array(lifeId)
        self.a[y:y + figure.shape[0], x:x + figure.shape[1]] = figure

    def base_alive_gen(self):
        mid = round(self.width / 2)
        self.a[mid - 1, mid] = self.a[mid, mid] = self.a[mid + 1, mid] = 1

    def random_gen(self):
        self.a = np.random.randint(2, size=(self.height, self.width))

    def check_border(self):
        for y in range(self.a.shape[0]):
            for x in range(self.a.shape[1]):
                if x + self.border >= self.a.shape[1] or x - self.border <= 0 or y + self.border >= self.a.shape[
                    0] or y - self.border <= 0:
                    self.a[y, x] = 0
        self.new_a = self.a.copy()

    def check_cell(self, y, x):
        cell = self.new_a[y, x]
        '''
		   123
		   405
		   678
		'''
        adj = [
            self.a[y + 1, x], self.a[y + 1, x + 1], self.a[y + 1, x - 1],
            self.a[y, x + 1], self.a[y, x - 1],
            self.a[y - 1, x], self.a[y - 1, x + 1], self.a[y - 1, x - 1]
        ]
        if cell:
            if sum(adj) != 2 and sum(adj) != 3:
                self.new_a[y, x] = 0
                not self.log or print(f"Cell in x{x}, y{y} is dead")

        # une cellule vivante possédant deux ou trois cellules voisines vivantes le reste, sinon elle meurt
        else:
            if sum(adj) == 3:
                self.new_a[y, x] = 1
                not self.log or print(f"Cell in x{x}, y{y} is born")
        # une cellule morte possédant exactement trois cellules voisines vivantes devient vivante (elle naît)

    def init_pygame(self):
        pygame.init()
        width = self.a.shape[1] * self.cell_size
        height = self.a.shape[0] * self.cell_size
        self.screen = pygame.display.set_mode((width, height))

    def show_map(self):
        # Crée une surface rectangulaire pour chaque case de la carte
        cell_surf = pygame.Surface((self.cell_size, self.cell_size))
        for y, row in enumerate(self.new_a):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if cell:
                    cell = (255, 255, 255)
                else:
                    cell = (0, 0, 0)
                cell_surf.fill(cell)
                self.screen.blit(cell_surf, rect)

        pygame.display.flip()

    def test(self, figure, yx=(0, 0), show=True):
        global EMERGENCY_END
        if yx == (0, 0):
            yx = (round(self.height / 2), round(self.width / 2))
        y, x = yx
        if isinstance(figure, str):
            figure = get_array(figure)

        if isinstance(figure, int):
            print("pass test", figure)
            for comb in range(2 ** 25):
                if comb == figure:
                    figure = np.zeros((5, 5), dtype=int)
                    for f_y in range(5):
                        for f_x in range(5):
                            figure[f_y, f_x] = (comb >> (f_y * f_x + f_x)) & 1
                            self.a[y:y + figure.shape[0], x:x + figure.shape[1]] = figure
                    break
        elif isinstance(figure, list):
            figure = np.array(figure)
            self.a[y:y + figure.shape[0], x:x + figure.shape[1]] = figure
        elif isinstance(figure, np.ndarray):
            self.a[y:y + figure.shape[0], x:x + figure.shape[1]] = figure
        result = self.run(show=show)
        return result

    def test_all_in(self, f_height=5, f_width=5, yx=(0, 0), range_list=range(6), show=True, log_day=True):
        global EMERGENCY_END
        if yx == (0, 0):
            yx = (round(self.height / 2), round(self.width / 2))
        new = np.zeros((f_height, f_width), dtype=int)
        counter = 0
        for comb in range(2 ** (f_height * f_width)):
            if comb in range_list:
                if show:
                    self.reset()
                for y in range(f_height):
                    for x in range(f_width):
                        new[y, x] = (comb >> (y * x + x)) & 1
                y, x = yx

                if sum(sum(new)) > 0:
                    self.a[y:y + new.shape[0], x:x + new.shape[1]] = new
                    print(f"Test number {comb} is running [lifeID]|{get_lifeId(new)}|")
                    result = self.results[get_lifeId(new)] = self.run(show=show, log_day=log_day)
                    print(f"Test number {comb} is termined : {result}")
                    if result[2] > 5:
                        yield {get_lifeId(new): result}

                counter += 1
                if counter == range_list[-1] + 1:
                    break

    def live(self):
        global EMERGENCY_END
        self.init_pygame()
        day = 1
        base_n_cell = last_n_cell = sum(sum(np.where(self.a, 1, 0)))
        count = 0

        while True:
            pygame.display.update()
            n_cell = sum(sum(np.where(self.a, 1, 0)))
            if n_cell != 0:
                purcent = round((n_cell - last_n_cell) / last_n_cell * 100)
            else:
                purcent = 0
            print(f"Day {day}, cells {n_cell}, evolution {'+' if last_n_cell <= n_cell else ''}{purcent}%")
            self.new_a = self.a.copy()

            for y in range(self.new_a.shape[0]):
                for x in range(self.new_a.shape[1]):
                    # print(x, y, a.shape)
                    if (y, x) == self.a.shape or x in [0, self.a.shape[1] - 1] or y in [0, self.a.shape[0] - 1]:
                        self.new_a[y, x] = 0
                    else:
                        self.check_cell(y, x)
            self.a = self.new_a.copy()
            self.show_map()
            sleep(self.delay)
            day += 1
            last_n_cell = n_cell
            if EMERGENCY_END:
                break

    def run(self, show=True, log_day=True):
        if show:
            self.init_pygame()
        day = 1
        pre_states = []
        base_n_cell = last_n_cell = sum(sum(np.where(self.a, 1, 0)))
        count = 0
        infinite = False

        while True:
            global EMERGENCY_END
            n_cell = sum(sum(np.where(self.a, 1, 0)))
            if n_cell != 0:
                purcent = round((n_cell - last_n_cell) / last_n_cell * 100)
            else:
                purcent = 0
            if log_day:
                print(f"Day {day}, cells {n_cell}, evolution {'+' if last_n_cell <= n_cell else ''}{purcent}%")

            self.new_a = self.a.copy()

            for y in range(self.new_a.shape[0]):
                for x in range(self.new_a.shape[1]):
                    # print(x, y, a.shape)
                    if (y, x) == self.a.shape or x in [0, self.a.shape[1] - 1] or y in [0, self.a.shape[0] - 1]:
                        self.new_a[y, x] = 0
                    else:
                        self.check_cell(y, x)
            self.a = self.new_a.copy()
            if show:
                self.show_map()

            if self.delay:
                sleep(self.delay)

            if last_n_cell == n_cell:
                count += 1
            else:
                count = 0

            last_n_cell = n_cell
            day += 1
            if EMERGENCY_END:
                print("=== STOPPED ===")
                return [base_n_cell, n_cell, day, infinite]

            if count == 5 or self.a.tolist() in pre_states:
                infinite = True
                print("=== TERMINED ===")
                return [base_n_cell, n_cell, day, infinite]
            elif n_cell == 0:
                print("=== TERMINED ===")
                return [base_n_cell, n_cell, day, infinite]

            pre_states.append(self.a.tolist())
            pre_states = pre_states[-50:]


def serial_test(range_list=range(21), height=150, width=150, cell_size=5, show=True):
    global closable
    data = {}
    lifeGame = LifeGame(delay=0, height=height, width=width, cell_size=cell_size)

    closable = False
    for result in lifeGame.test_all_in(range_list=range_list, log_day=True, show=show):
        data.update(result)
        print("(added result)")
        if EMERGENCY_END:
            break

    # open("lifeSave.json", 'w+').write(json.dumps(data))

    print("Analyze of results..")
    top = {}

    def convert(o):
        if isinstance(o, np.int32):
            return int(o)
        raise TypeError

    try:
        not exists("lifeSave.json") or data.update(json.loads(open("lifeSave.json", 'r').read()))
        data = json.dumps(data, default=convert)
    except Exception as error:
        print(f"error json: {error}\nwriting brut data...")
        not exists("lifeSave.json") or data.update(literal_eval(open("lifeSave", 'r').read()))
        open("lifeSave", 'w+').write(str(data))
    else:
        open("lifeSave.json", 'w+').write(data)
    closable = True

    for value in data.values():
        value = value[2]
        for key in data.keys():
            if data[key][2] == value:
                if value not in top.keys():
                    top[value] = []
                top[value].append(key)

    for best in list(reversed(sorted(list(top.keys()))))[:3]:
        print(f"\n===== {best} day =====")
        c = 0
        for i, element in enumerate(top[best]):
            print(c * '\t' + element)
            for line in get_lists(element):
                print(c * '\t' + str(line))
            c += 1


def resume_test(limit=50):
    if exists("lifeSave.json"):
        data = json.loads(open("lifeSave.json", 'r').read())
    elif exists("lifeSave"):
        data = literal_eval(open("lifeSave", 'r').read())
    else:
        data = {}
    test_number = len(data)
    serial_test(range_list=range(test_number, test_number + limit))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    args = sys.argv[1:]
    if len(args) == 0:
        args = ['']
    if args[-1] == "nogui":
        show = False
    else:
        show = True
    if args[0] == "test":
        lifeGame = LifeGame(delay=0, height=150, width=150, )
        if len(args) > 2:
            if args[1] == "id":
                lifeId = args[2]
                lifeGame.test(lifeId, show=show)
            elif args[1] == "number":
                lifeGame.test(int(args[2]), show=show)
    elif args[0] == "resume":
        if len(args) > 1:
            if len(args) > 2:
                test_number = int(args[1])
                serial_test(range_list=range(test_number, int(args[2])), show=show)
            elif "+" in args[1]:
                limit = int(args[1][1:])
                print(f"resume to +{limit}")
                resume_test(limit=limit)
            else:
                test_number = int(args[1])
                serial_test(range_list=range(test_number, test_number + 50), show=show)
        else:
            resume_test()
    elif args[0] == "random":
        lifeGame = LifeGame(delay=0, height=150, width=150, cell_size=5)
        lifeGame.random_gen()
        lifeGame.run(show=show)
    elif args[0] == "live":
        lifeGame = LifeGame(delay=0, height=150, width=150)
        if len(args) > 2:
            if args[1] == "id":
                lifeId = args[2]
                lifeGame.set(lifeId)
                lifeGame.live()
        else:
            lifeGame.base_alive_gen()
            lifeGame.live()
    else:
        lifeGame = LifeGame(delay=0.5, height=50, width=50, cell_size=15)
        lifeGame.base_alive_gen()
        lifeGame.live()
