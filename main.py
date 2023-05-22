from time import process_time

from sudoku import ExcaliburSudoku
print("Solving example 1")
sudoku = ExcaliburSudoku.from_json("examples/test/expert.json")
sudoku.print_board()
print("Solving...")
now = process_time()
print(sudoku.solve())
print("Solved!")
sudoku.print_board()
print(f"Time: {process_time() - now}")
print(f"Steps: {ExcaliburSudoku.step_count}")
