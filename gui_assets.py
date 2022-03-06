# Colors used in the GUi
COLORS = {
    'BLACK': (0,0,0),
    'WHITE': (255,255,255),
    'GRAY': (128, 128, 128),
    'GREEN': (0,255,0),
    'RED': (255,0,0),
}

# Helper function to flip the color of a chess board cell.
def flip_cell_color(cell_color):
    if cell_color == COLORS['WHITE']:
        return COLORS['GRAY']
    return COLORS['WHITE']