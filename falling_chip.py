class FallingChip(object):

    isFalling = True
    jump_count = 1

    def __init__(self, x, y, rest_y, color, column):
        self.x = x
        self.y = y
        self.rest_y = rest_y
        self.color = color
        self.column = column

    def fell(self):
        return not self.isFalling

    def get_xy(self):
        return self.x, self.y

    def move(self):

        if self.y + self.jump_count**2 / 5 > self.rest_y:
            self.y = self.rest_y
            self.isFalling = False

        else:
            self.y += int(self.jump_count**2 / 3)

        self.jump_count += 1