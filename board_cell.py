import pygame

from gui_assets import COLORS

class BoardCell:

    def __init__(self, row, col, size, color, num_rows):
        self.row = row
        self.col = col
        self.size = size
        self.has_queen = False
        self.color = color 

        self.x = row * size
        self.y = col * size

        self.num_rows = num_rows

    def get_position(self):
        return (self.row, self.col)

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

