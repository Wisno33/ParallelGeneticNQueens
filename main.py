import argparse
import os
import sys
from multiprocessing import Process, Value, Array
import time

from n_queens import n_queens

def main():

    # Set program description and arguments.
    parser = argparse.ArgumentParser(description='A n-queens solver ' +
                                    'via a genetic algorithm.')

    # Optional argument specifies number of suprocesses to run.
    parser.add_argument('--n_jobs', metavar='', type=int, required=False,
                        default=1, help='Number of subprocesses ' +
                        'to run, limited to number logical processors ' +
                        'on system. Use -1 to use all processors.')

    # Optional argument specifies if the GUI version should be used.
    parser.add_argument('--gui', metavar='', action=argparse.BooleanOptionalAction,
                        required=False, help='Runs in a GUI instead of in the ' + 
                        'terminal n is limited to 8.')

    # Get the arguments.
    args = parser.parse_args()

    if args.gui:
        from gui import GUI
        window = GUI()
        window.main_loop()
    else:

        # Validate the number of subprocesses, if -1 set to total #processors.
        if args.n_jobs == -1:
            args.n_jobs = os.cpu_count()
        elif args.n_jobs > os.cpu_count() or args.n_jobs < -1:
            print(f'Invalid selection for n_jobs. Value for n_jobs should ' +
                    f'not exceed {os.cpu_count()} or be below -1.')
            exit(0)

        processes = [None] * args.n_jobs

        n = int(input('Enter a value for n: '))

        # Set shared memory variable for supprocesses.
        is_solved = Value('i', 0) # Set to 1 when a solution is found. Used to end subprocesses.
        solution_array = Array('i', n) # Array of integers (ctype)

        # Create subprocesses to execute the n_queens function with arguments
        # n (number of queens) and the shared array for solution storage.
        for i in range(len(processes)):
            processes[i] = Process(target=n_queens, args=(n, is_solved, solution_array))

        start = time.time() # Start of execution time.

        # Begin execution of subprocesses.
        for process in processes:
            process.start()

        # End execution of subprocesses.
        for process in processes:
            process.join()

        end = time.time() # End of execution time.

        if is_solved.value == 0:
            print(f'No solution to {n}-queens exists.')
            return

        solution = list()

        for i in range(len(solution_array)):
            solution.append(solution_array[i])

        # Print the solution and the board.
        print(f'The solution to {n}-queens is {solution}. This solution ' + 
                f'took {round(end-start, 2)} seconds to compute')

        board = list()

        for _ in solution:
            board.append(['X'] * n)

        for i in range(len(solution_array)):
            board[solution_array[i]][i] = 'Q'

        for row in board:
            for cell in row:
                print(cell, end=' ')
            print()


if __name__ == '__main__':
    main()