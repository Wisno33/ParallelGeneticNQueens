import pygame

from gui_assets import COLORS

# Board cell object for the chess board gui.
class BoardCell:

    def __init__(self, row, col, size, color, num_rows):
        self.row = row 
        self.col = col
        self.size = size
        self.has_queen = False
        self.color = color 

        # Pixel coords
        self.x = row * size 
        self.y = col * size

        self.num_rows = num_rows

    # Draw the cell on the surface.
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))

