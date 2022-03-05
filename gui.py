import pygame
import pygame_menu

# Colors used in the GUi
COLORS = {
    'BLACK': (0,0,0),
    'WHITE': (255,255,255),
    'GRAY': (128, 128, 128),
    'GREEN': (0,255,0),
    'RED': (255,0,0),
}

class GUI:

    # Create and start the GUI.
    def __init__(self):
        pygame.init()
        self.width, self.height = self.get_window_percentage(.60)
        self.window = pygame.display.set_mode((self.width, self.height), vsync=True)
        self.start_menu() # Set the GUI window to the start window.

    def get_window_percentage(self, percentage):

        return (int(1600*percentage), int(1300*percentage))

    # GUI start window allows data entry and selection.
    def start_menu(self):

        self.window.fill(COLORS['WHITE'])

        pygame.display.set_caption('Genetic n-queens')

        pygame.display.update()

        # Initialize the selector values.
        self.n = ('None', 0)
        self.pop_size = ('None', 0)

        # Create the welcome and selection menu.
        self.menu = pygame_menu.Menu('Welcome', self.width, self.height, theme=pygame_menu.themes.THEME_DEFAULT)

        # Selector for n.
        self.menu.add_selector('N-Queens:', [('Select a value for n', 0), ('1', 1), ('2', 2), ('3', 3),
                                ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8)], onchange=self.n)
        
        # Selector for population size.
        self.menu.add_selector('Population Size:', [('Select a value for the population', 0), ('4', 4), 
                                ('8', 8), ('16', 16), ('32', 32), ('64', 64)], onchange=self.pop_size)
                        
        self.menu.add_button('Compute!', self.run_n_queens) # Begin execution of n-queens.
        self.menu.add_button('Information', self.toggle_information_labels) # Display infomation.
        self.information_labels_visible = False # Information is not shown to start.
        self.quit_button = self.menu.add_button('Quit', pygame_menu.events.EXIT) # Exit 

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

        self.information_labels.append(self.menu.add_label('Instructions', max_char=-1, font_size=25))
        self.information_labels.append(self.menu.add_label('1) Select a value for n (1-8 inclusive).',
                                                            max_char=-1, font_size=15))
        self.information_labels.append(self.menu.add_label('2) Select a value for the initial population ' +
                                                            '(4-64 powers of 2 inclusive).', max_char=-1, font_size=15))
        self.information_labels.append(self.menu.add_label('3) Select a compute to begin the animation.', 
                                                            max_char=-1, font_size=15))
     
        # Re-add the quit button at the end of the information.
        self.quit_button = self.menu.add_button('Quit', pygame_menu.events.EXIT) # Exit 
        
    def hide_information_labels(self):

        for label in self.information_labels:
            self.menu.remove_widget(label)

    def draw(self):

        self.window.fill(COLORS['WHITE'])

        for row in range(self.n):
            for cell in row:
                cell.draw(self.window)

    def run_n_queens(self):
        
        self.n = self.n[1]
        self.pop_size = self.pop_size[1]

        if n == 0 or population_size == 0:
            return

        # Destroy the start menu for now.
        self.menu.disable()

        self.draw()

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