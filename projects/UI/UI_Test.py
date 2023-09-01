import sys
from time import sleep
from random import choice, randint
import curses
from curses import wrapper
from curses.textpad import rectangle, Textbox
from os import get_terminal_size
from threading import Thread

def writing(string, y=1, x=0, speed=0.01, std=curses.window):
    for char in string:
        if char == "\n":
            y += 1
            x = 0
            
        std.addstr(y, x, char)
        std.refresh()
        x+=1
        sleep(speed)

def load(value, max):
    columns = get_terminal_size().columns-2
    calc = value/max
    n = int(calc*columns)
    return f"[{'#'*n}{(columns-n)*'-'}]{'{:.2f}'.format(round(calc*100, 2))}%"

def get_pos(pos, auto=True):
    t_size = get_terminal_size()
    if auto:
        pos = (t_size.lines - 2, pos[1])
    elif pos[0] > t_size.lines:
        pos[0] = pos[0] / last_size.lines * t_size.lines
    elif pos[1] > t_size.columns:
        pos[1] = pos[1] / last_size.columns * t_size.columns

    return pos

def show_load(std, pos=(None, 0), max=1000, speed=0.01, frame_interval=1):
    last_size = get_terminal_size()
    # std.clear()
    if pos[0] == None:
        auto = True
        pos = get_pos(pos, auto)
    counter = 0
    i = 0
    resized = False
    while counter != max + 1:
        sleep(speed)
        std.addstr(0, 0, f"resized {resized}")
        std.addstr(pos[0], pos[1], load(counter, max))
        counter += 1
        i += 1
        if last_size != get_terminal_size():
            resized = True
            last_size = get_terminal_size()
            pos = get_pos(pos, auto)
            std.clear()
        if i == frame_interval:
            pos = get_pos(pos, auto)
            std.refresh()  # pas besoin de clear avec cmd("clear") ou std.clear() et de reafficher
            i = 0
    std.getch()  # attends que l'utilisateur appuie sur une touche pour fermer
    pass

def add_more(std):
    stdout = sys.stdout.read()
    std.clear()
    show_load(std)

def test(std):
    std.clear()  # vider le terminal
    std.addstr("hello world", curses.A_UNDERLINE)
    std.addstr("exemple invisible", curses.A_COLOR)
    std.addstr("et si", curses.A_ITALIC)
    std.getch()  # attends que l'utilisateur appuie sur une touche pour fermer

def m(n1, n2):
    return n1*n2

def wtf(std):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    CYRE = curses.color_pair(1)
    REGRE = curses.color_pair(2)
    std.clear()  # vider le terminal
    std.addstr(9, 10, "hello world")
    std.addstr(10, 10, "hello world", curses.A_DIM)
    std.addstr(11, 10, "hello world", CYRE)
    std.addstr(12, 10, "hello world", REGRE | curses.A_REVERSE | curses.A_BOLD)
    colors = []
    for i in range(100):
        std.clear()
        curses.init_pair(55, randint(1, curses.COLORS-1), randint(1, curses.COLORS-1))
        std.addstr((m(*get_terminal_size())-1)*"a", curses.color_pair(55))
        sleep(0.1)
        std.refresh()

    std.getch()  # attends que l'utilisateur appuie sur une touche pour fermer

def wintest(std):
    std.clear()
    std.addstr("Nous allons passer à l'autre fenetre bientot...")
    std.getch()
    newin = curses.newwin(1, 20, 10, 10)
    wrapper(test)
    std.clear()
    std.addstr("Okay")
    std.getch()

def effect(std):
    curses.init_pair(22, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_BLACK = curses.color_pair(22)
    std.clear()
    std.addstr("Nous allons passer à l'autre fenetre bientot...")
    std.getch()
    pad = curses.newpad(100, 100)
    std.refresh()
    # while True:
    for i in range(100):
        for j in range(26):
            char = chr(67 + j)
            pad.addstr(char, GREEN_BLACK)

    for i in range(50):
        std.clear()
        std.refresh()
        # pad.refresh(0, i, 5, i, 25, 75+i)  # window effect
        # pad.refresh(0, i, 5 + i, i, 10+i, 25 + i)  # dvd
        pad.refresh(i, 0, 0, 0, 20, 20) # scroll down)
        sleep(0.2)
    std.getch()

def game(std: curses.window = None):
    std = std
    std.nodelay(True)
    x, y = 0, 0
    while True:
        try:
            key = std.getkey()
            match key:
                case "KEY_LEFT":
                    x -= 1
                case "KEY_RIGHT":
                    x += 1
                case "KEY_UP":
                    y -= 1
                case "KEY_DOWN":
                    y += 1
        except:
            key = None
        else:
            std.clear()
            std.addstr(y, x, "0")
            std.refresh()

def box_border(std: curses.window = None):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    CYRE = curses.color_pair(1)
    REGRE = curses.color_pair(2)
    std = std
    win = curses.newwin(3, 18, 2, 2)
    box = Textbox(win)

    std.attron(REGRE)
    std.border()
    std.attroff(REGRE)
    std.attron(CYRE)
    rectangle(std, 1, 1, 5, 20)
    std.attroff(CYRE)
    std.refresh()

    box.edit()
    text = box.gather().strip().replace("\n", '')

    std.addstr(15, 10, f"Your text : {text}")

    std.getch()

def main(std: curses.window = None):
    std = std
    curses.echo()
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
    REGRE = curses.color_pair(2)
    std.attron(REGRE)
    std.border()
    std.attroff(REGRE)
    std.move(10, 20)
    std.refresh()
    while True:
        key = std.getkey()
        if key == "²":
            break

def write_load(std, string="Hey salut les gens comment ça va aujourd'hui ?", speed=0.1):
    std = std
    std.clear()
    Thread(target=writing, args=(string, 2, 0, speed, std,)).start()
    show_load(std, max=len(string), speed=speed)

print(' '.join(i for i in globals()))
while True:
    f = input("Function: ")
    if f in globals().keys():
        wrapper(globals()[f])
        break

# wrapper(write_load)
# # wrapper(game)
# print("after")