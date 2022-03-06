# ParallelGeneticNQueens

A parallelized implementation of an n-queens genetic algorithm. This project has both a command line and GUI options.

The command line option allows up to 100 queens (although options above 10 are time intensive). The population size is set to 4, when using the command line. There are two optional flags for the command line option. Firstly, is the '--n_jobs' flag, this option allows the user to specify the number of logical processors to use during execution of the program, the default for this flag is n_jobs=1. If the user tries to the amount of logical processors present on the system, the program will not execute and a message will be returned to the user specifying the maximum value allowed for the argument. A special option for this argument is -1 which specifies use all cores. The other flag for the command line is '--log', this flag specifies if the user wishes to see the current generation number and that generations maximum fitness score, note this is possible with more than 1 processor (i.e. n_jobs>1). If there are multiple parallel processes running each process will have its own generation counter. Note: order cannot be guaranteed for printed information if n_jobs>1.

The GUI option can be activated via the '--gui' flag. If this flag is used the aforementioned flags will be discarded as they are not relevant to the GUI option.The GUI allows for 1-8 queens, and unlike the command line option, the option to select the population size. The options for the population size are the powers of 2 from 4-64. The GUI menu page also has information on how to use if needed.


To run the project simply use 'python main.py'. If the --gui flag is not used, the user will be prompted for a n value. After entry the algorithm will compute the answer, if '--log' was set during execution the relevant items will be printed. After a solution state is found the time taken, the solution, and a text chess board representing the solution will be displayed. If no solution exists the user will be notified.

If the '--gui' flag is selected the user will be shown a menu window from where selections for n, population size, and animation speed are available. All of these selections must be made before the user will be allowed to run the algorithm. Once ready the user can select the 'Compute!' option and visualize the progress. The visualization will show the state with the maximum fitness for each generation. Once done the animation will stop. The user can then exit or press esc to return to the menu and re-run. If no solution is possible the user will be returned to the menu, and notified that no solution is possible.


# Requirements
-- Python 3.10.1
-- pygame 2.2.1
-- pygame-menu 4.0.2
-- Pillow 9.0.0
