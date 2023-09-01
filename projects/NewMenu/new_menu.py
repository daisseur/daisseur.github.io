import curses
from curses import wrapper
from curses.textpad import rectangle, Textbox
from time import sleep

window = curses.initscr()
if curses.has_colors():
    curses.start_color()
curses.curs_set(0)
curses.noecho()
window.keypad(1)

example1 = ["Yes", "No"]
example2 = {"title": 'Who are you ?',
            "Hacker":
                {"title": "What type of hecker are u ?",
                 "Black hat": "He is a black hat",
                 "Grey hat": "He's a grey hat",
                 "White hat": {"title": "You're really a white hat ?",
                               "YES": "A WHITE HAT",
                               "Not really": "not really"}
                 },
            "Normal people":
                {"title": "ORIENTATION",
                 "Gay": "Gay",
                 "Hetero": "hetero",
                 "Others": "others"}
            }


class Menu:
    def __init__(self, choices=example1, arb_choices=example2, title="", border_style: list[int] = [curses.COLOR_BLUE, curses.COLOR_BLACK], selected_style: list[int] = [curses.COLOR_WHITE, curses.COLOR_BLUE], xy: tuple = None, log__var=False, std=window):
        self.std = std
        self.selected = 0
        self.log__var = log__var
        self.show_log__var = self.log__var
        self.log = []
        self.title = title
        self.arb_choices = arb_choices
        self.choices = choices
        self.x, self.y = xy or (10, 10)
        if (self.x, self.y) != (10, 10):
            self.show_log__var = False

        self.border_style = border_style
        self.selected_style = selected_style

    class Error(Exception):
        def __init__(self, message):
            self.message = message

    def add_log(self, *args):
        if self.log__var:
            self.log.append(f"[LOG] {''.join(str(arg) for arg in args)}")

    def show_log(self):
        if self.log__var:
            print("\n".join(self.log))

    def menu_log(self, x, y, string):
        if self.log__var:
            self.std.addstr(x, y, string)

    def set_border(self):
        curses.init_pair(1, *self.border_style)

        blue = curses.color_pair(1)
        self.std.attron(blue)
        self.std.border()
        self.std.attroff(blue)

    def set_title(self, title=None):
        if title:
            self.title = title
        x, y = self.x - 2, self.y
        self.std.addstr(x, y, self.title or "", curses.A_BOLD)

    def set_choices(self, selected=0):
        self.menu_log(2, 5, str(selected))
        style = self.selected_style
        x, y = self.x, self.y

        for index in range(len(self.choices)):
            if index == selected:
                if len(self.selected_style) == 2:
                    curses.init_pair(12, *self.selected_style)
                    color = curses.color_pair(12)
                    self.std.attron(color)
                    self.std.addstr(x, y, self.choices[index])
                    self.std.attroff(color)
                else:
                    self.std.addstr(x, y, self.choices[index], *style)
            else:
                self.std.addstr(x, y, self.choices[index])
            x += 1

    def user_key(self, key):
        if key == 27:
            print("EXIT")
            exit()
        elif key == curses.KEY_DOWN:
            self.menu_log(3, 5, "DOWN")
            self.selected = self.selected + 1
            if self.selected > len(self.choices) - 1:
                self.selected = self.selected % len(self.choices)
        elif key == curses.KEY_UP:
            self.selected = (self.selected - 1)
            if self.selected <= 0:
                self.selected = self.selected % len(self.choices)
            self.menu_log(3, 5, "UP")
        elif key == 10 or key == 261:
            self.menu_log(3, 5, "ENTER")
            return True

    def show_all(self, arb_choices=None, log__var=None):
        self.log__var = log__var or self.log__var
        self.arb_choices = arb_choices or self.arb_choices
        element = self.arb_choices
        while True:
            self.selected = 0
            self.choices = []
            for i in enumerate(element):
                if i[1] == "title":
                    self.title = element["title"]
                else:
                    self.choices.append(i[1])

            self.add_log(f"== {self.title} ==:", self.choices)
            res = self.show()
            self.title = None
            self.add_log("Selected:", res)

            element = element[res]

            if not isinstance(element, dict):
                self.add_log(element)
                self.show_log()
                return element

    def show(self, std=None):
        if std:
            self.std = std
        curses.noecho()
        curses.cbreak()
        self.std.leaveok(True)
        key = 0
        while True:

            self.std.clear()
            if self.user_key(key) is True:
                self.std.clear()
                curses.endwin()
                return self.choices[self.selected]

            self.set_border()
            self.menu_log(5, 10, f"Key : {key}")
            self.set_title()
            self.set_choices(selected=self.selected)

            self.std.refresh()
            key = self.std.getch()

res = Menu(["Hacker -->", "Se branler -->", "Faire des choses -_-", "Ou rien faire !!!", " ", "Mais bref"], title="Exemple Simple").show()

log = Menu(title="Activer le mode LOG ?").show_all(arb_choices={"Oui": True, "Non": False})

color_dict = {
    "Blue": curses.COLOR_BLUE,
    "Black": curses.COLOR_BLACK,
    "White": curses.COLOR_WHITE,
    "Red": curses.COLOR_RED,
    "Green": curses.COLOR_GREEN,
    "Yellow": curses.COLOR_YELLOW,
    "Magenta": curses.COLOR_MAGENTA,
    "Cyan": curses.COLOR_CYAN,
    " ": [1, 0]
}

color1 = Menu(title="Choisis la couleur de police de la sélection").show_all(arb_choices=color_dict)
if isinstance(color1, list):
    selected_style = color1
else:
    selected_style = [color1, Menu(title="Choisis la couleur d'arrière plan de la sélection").show_all(arb_choices=color_dict)]

print(Menu(log__var=log, selected_style=selected_style).show_all())
