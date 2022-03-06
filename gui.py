import pygame
import pygame_menu
from PIL import Image

from gui_assets import COLORS, flip_cell_color
from board_cell import BoardCell
from n_queens import n_queens

class GUI:

    # Create and start the GUI.
    def __init__(self):
        pygame.init()
        self.width, self.height = self.get_window_percentage(.60)
        self.window = pygame.display.set_mode((self.width, self.height), vsync=True)
        self.data_bar_space = (0,0)
        self.start_menu() # Set the GUI window to the start window.

    def get_window_percentage(self, percentage):

        return (int(1200*percentage), int(1200*percentage))

    def set_n(self, n, args=None):
        self.n = n[0]

    def set_pop_size(self, pop_size, args=None):
        self.pop_size = pop_size[0]

    def set_speed(self, speed, args=None):
        self.speed = speed[0][1]

    # GUI start window allows data entry and selection.
    def start_menu(self, notify=False, no_sol_n=None):

        self.window.fill(COLORS['WHITE'])

        pygame.display.set_caption('Genetic n-queens')

        pygame.display.update()

        # Initialize the selector values.
        self.n = ('None', 0)
        self.pop_size = ('None', 0)
        self.speed = 1

        # Create the welcome and selection menu.
        self.menu = pygame_menu.Menu('Welcome', self.width, self.height, theme=pygame_menu.themes.THEME_DEFAULT)

        # Notify the user no solution exists.
        if notify:
            self.notify_no_solution = self.menu.add.label(f'No solution to {no_sol_n}-queens.', 
                                                            max_char=-1, font_size=20)   

        # Selector for n.
        self.menu.add.selector('N-Queens:', [('Select a value for n', 0), ('1', 1), ('2', 2), ('3', 3),
                                ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8)], onchange=self.set_n)
        
        # Selector for population size.
        self.menu.add.selector('Population Size:', [('Select a value for the population', 0), ('4', 4), 
                                ('8', 8), ('16', 16), ('32', 32), ('64', 64)], onchange=self.set_pop_size)
        
        self.menu.add.selector('Animation Speed:', [('1', 1), ('2', 0.5), 
                                ('5', 0.2), ('10', 0.1)], onchange=self.set_speed)
                        
        self.menu.add.button('Compute!', self.run_n_queens) # Begin execution of n-queens.
        self.menu.add.button('Information', self.toggle_information_labels) # Display infomation.
        self.information_labels_visible = False # Information is not shown to start.
        self.quit_button = self.menu.add.button('Quit', pygame_menu.events.EXIT) # Exit 

        # Run the menu until user exits the menu to the main window.
        self.menu.mainloop(self.window)

    # Used to toggle the display of information labels when selected
    def toggle_information_labels(self):

        # Show information if not visible.
        if not self.information_labels_visible:
            self.display_information_labels()
            self.information_labels_visible = True
        # Hide information if visible.
        else:
            self.hide_information_labels()
            self.information_labels_visible = False


    # When the information button is selected, display the information.
    def display_information_labels(self):
        
        # Remove the exit widget for replacement.
        self.menu.remove_widget(self.quit_button)

        self.information_labels = list()

        self.information_labels.append(self.menu.add.label('Instructions', max_char=-1, font_size=25))
        self.information_labels.append(self.menu.add.label('1) Select a value for n (1-8 inclusive).',
                                                            max_char=-1, font_size=15))
        self.information_labels.append(self.menu.add.label('2) Select a value for the initial population ' +
                                                            '(4-64 powers of 2 inclusive).', max_char=-1, font_size=15))
        self.information_labels.append(self.menu.add.label('3) Select a compute to begin the animation.', 
                                                            max_char=-1, font_size=15))
     
        # Re-add the quit button at the end of the information.
        self.quit_button = self.menu.add.button('Quit', pygame_menu.events.EXIT) # Exit 
        
    # Remove / hide the information section.
    def hide_information_labels(self):

        for label in self.information_labels:
            self.menu.remove_widget(label)

    def make_board(self):

        size = (self.width - self.data_bar_space[0]) // self.num_chess_cells_1D

        board = list()

        for l in range(self.num_chess_cells_1D):
            board.append([None] * self.num_chess_cells_1D)

        cell_color = COLORS['WHITE']

        for i in range(self.num_chess_cells_1D):
            for j in range(self.num_chess_cells_1D):
                cell = BoardCell(i, j, size, cell_color, self.num_chess_cells_1D)
                board[i][j] = cell
                cell_color = flip_cell_color(cell_color)
            if self.num_chess_cells_1D % 2 == 0:
                cell_color = flip_cell_color(cell_color)

        self.board = board

    def draw_board(self):

        size = (self.width - self.data_bar_space[0]) // self.num_chess_cells_1D

        for row in self.board:
            for cell in row:
                cell.draw(self.window)
                if cell.has_queen:
                    self.window.blit(self.queen_image, (cell.x,cell.y))

    def set_queen_size(self, size):

        queen_image = Image.open('queen.png')
        queen_image = queen_image.resize((int(size),int(size)))
        queen_image.save('queen_out.png')
        # Image of a queen chess piece.
        self.queen_image = queen_image = pygame.image.load('queen_out.png')

    def clear_queens(self):

        for row in self.board:
            for cell in row:
                cell.has_queen = False
            
    def draw_board_border(self):

        size = (self.width - self.data_bar_space[0]) // self.num_chess_cells_1D
        
        lowest_y = self.board[-1][-1].y + size

        print(lowest_y)
    
        pygame.draw.line(self.window, COLORS['BLACK'], (self.height, 0), (self.height, ((self.n * size) - self.data_bar_space[0])))

        print( (0, self.height), (((self.n * size) - self.data_bar_space[0]), self.height))
    
    # Draw the items on the board, queens chess board and data.
    def draw(self):

        self.window.fill(COLORS['WHITE'])

        self.draw_board()
        #self.draw_board_border()

        pygame.display.update()

    def run_n_queens(self):
        
        self.n = self.n[1]
        self.num_chess_cells_1D = self.n
        self.pop_size = self.pop_size[1]

        if self.n == 0 or self.pop_size == 0:
            return

        # Destroy the start menu for now.
        self.menu.disable()

        self.make_board()
        self.set_queen_size((self.width - self.data_bar_space[0]) // self.num_chess_cells_1D)

        self.draw()

        solution = [0] * self.n
        is_solved = lambda: None; is_solved.value = 0

        n_queens(self.n, is_solved, solution, False, original_pop_size=self.pop_size, gui_window=self)

        self.draw()

        if is_solved.value == 0:
            pygame.time.delay(500)
            self.start_menu(True, self.n)


    def main_loop(self):

        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.start_menu()

        pygame.quit()