
class Snake:
    def __init__(self, xy: tuple, head_color=(255, 255, 0), tail_color=(255, 255, 255)):
        self.x, self.y = xy
        self.head_color = head_color
        self.tail_color = tail_color
        self.lasts_xy = [self.get_pos()]
        self.direction = "N"
        self.parts_xy = []

    def add_part(self):
        for co in reversed(self.lasts_xy[:-1]):
            if co != self.get_pos() and co not in self.parts_xy:
                self.parts_xy.append(co)
                break

    def update_part(self):
        for index in range(len(self.parts_xy)):
            self.parts_xy[index] = self.lasts_xy[-2-index]

    def get_pos(self):
        return (self.x, self.y,)

    def update_direction(self):
        if len(self.lasts_xy) > 1:
            last_xy, actual_xy = self.lasts_xy[-2], self.lasts_xy[-1]
            if actual_xy[0] < last_xy[0]:
                self.direction = "W"
            elif actual_xy[0] > last_xy[0]:
                self.direction = "E"
            if actual_xy[1] < last_xy[1]:
                self.direction = "N"
            elif actual_xy[1] > last_xy[1]:
                self.direction = "S"
        return self.direction

    def downgrade(self):
        self.lasts_xy = self.lasts_xy[:-1]
        self.update_part()
        return self.get_pos()

    def check_lasts(self):
        for index in range(len(self.lasts_xy)):
            if self.lasts_xy[index] == self.get_pos():
                return True

    def update(self):
        self.lasts_xy.append(self.get_pos())
        if len(self.parts_xy) > 100:
            self.lasts_xy
        self.update_direction()
        self.update_part()
        return self.get_pos()

    def move_up(self):
        self.y -= 1
        return self.update()

    def move_down(self):
        self.y += 1
        return self.update()

    def move_right(self):
        self.x += 1
        return self.update()

    def move_left(self):
        self.x -= 1
        return self.update()

    def move(self):
        self.update()
        dir_to_move = {
            "N": self.move_up,
            "S": self.move_down,
            "E": self.move_right,
            "W": self.move_left
        }
        dir_to_move[self.direction]()
        return self.get_pos()
