"""
Solves 9x9 Sudoku puzzles using a constraint programming approach with the PuLP package

Usage:
	puzzle = [(row, col, value), ...]    # rows and cols range from 0-8, and values range from 1-9 (inclusive)
	solver = Solver(puzzle)
	status = solver.solve_puzzle()
	if status == 'Optimal':
		solver.write_solution_to_text('filename.txt')
"""

from re import findall
from pulp import *


class Solver:
	def __init__(self, starting_cells: list[tuple[int, int, int]]):
		"""Initialize the constraint programming problem, decision variables, and known cells,
		starting cells are in the format [(row, col, value)...]"""

		self.prob = LpProblem('Sudoku')  # no objective, just a list of constraints
		self._all_cells = self._set_decision_variables()
		self._set_fixed_constraints()
		self._starting_cells = starting_cells
		self._set_constraint_starting_cells(self._starting_cells)

	@staticmethod
	def _set_decision_variables() -> dict:
		"""Set up the decision variables for a 9x9 Sudoku grid
		81 cells x 9 possible values = 729 variables (each of them a Binary variable)"""

		return LpVariable.dicts("Cell",
								[(row, col, value)
								 for row in range(0, 9)
								 for col in range(0, 9)
								 for value in range(1, 10)],
								0, 1, LpBinary)

	def _set_fixed_constraints(self) -> None:
		"""Set up the constraints for a 9x9 Sudoku grid"""

		# constraint: every cell can only take on a single value
		for row in range(0, 9):
			for col in range(0, 9):
				self.prob += (
						lpSum([self._all_cells[(row, col, value)] for value in range(1, 10)]) == 1
				)

		# constraint: every value (1-9) must be seen exactly once per row
		for value in range(1, 10):
			for row in range(0, 9):
				self.prob += (
						lpSum([self._all_cells[(row, col, value)] for col in range(0, 9)]) == 1
				)

		# constraint: every value (1-9) must be seen exactly once per column
		for value in range(1, 10):
			for col in range(0, 9):
				self.prob += (
						lpSum([self._all_cells[(row, col, value)] for row in range(0, 9)]) == 1
				)

		# constraint: every value (1-9) must be seen exactly once per box
		for value in range(1, 10):
			for row_offset in (0, 3, 6):
				for col_offset in (0, 3, 6):
					self.prob += (
							lpSum(
								[self._all_cells[(row + row_offset, col + col_offset, value)] for row in range(0, 3) for
								 col in range(0, 3)]) == 1
					)

	def _set_constraint_starting_cells(self, starting_cells) -> None:
		"""Add known cells to the problem as a constraint"""
		for row, col, val in starting_cells:
			if val > 0:  # a 0 is an empty cell
				self.prob += self._all_cells[(row, col, val)] == 1

	def solve_puzzle(self) -> LpStatus:
		"""Solves the puzzle; returns status from the solver"""
		self.prob.solve(PULP_CBC_CMD(logPath=r'path.lp'))
		return LpStatus[self.prob.status]

	def parse_solution(self) -> list[tuple[int, int, int]]:
		"""Returns the puzzle solution in format [(row, col, value)...]"""
		re_string = r"""\d+"""
		solution = []

		for k, v in self.prob.variablesDict().items():
			if value(v) == 1:
				row, col, val = findall(re_string, k)
				solution.append((int(row), int(col), int(val)))

		return solution

	def write_solution_to_text(self, filename) -> None:
		"""Write solution to the specified file"""

		with open(filename, 'w') as f:
			for r in range(0, 9):
				if r in (0, 3, 6):
					f.write("+-------+-------+-------+\n")
				for c in range(0, 9):
					for v in range(1, 10):
						if self._all_cells[(r, c, v)].value() == 1:
							if c in (0, 3, 6):
								f.write("| ")
							f.write(str(v) + " ")
							if c == 8:
								f.write("|\n")
			f.write("+-------+-------+-------+")


if __name__ == '__main__':

	# from extremesodoku.info (Extreme difficulty puzzle)
	hard_puzzle = [(0, 0, 5),
				   (1, 0, 6),
				   (3, 0, 8),
				   (4, 0, 4),
				   (5, 0, 7),
				   (0, 1, 3),
				   (2, 1, 9),
				   (6, 1, 6),
				   (2, 2, 8),
				   (1, 3, 1),
				   (4, 3, 8),
				   (7, 3, 4),
				   (0, 4, 7),
				   (1, 4, 9),
				   (3, 4, 6),
				   (5, 4, 2),
				   (7, 4, 1),
				   (8, 4, 8),
				   (1, 5, 5),
				   (4, 5, 3),
				   (7, 5, 9),
				   (6, 6, 2),
				   (2, 7, 6),
				   (6, 7, 8),
				   (8, 7, 7),
				   (3, 8, 3),
				   (4, 8, 1),
				   (5, 8, 6),
				   (7, 8, 5)]

	solver = Solver(hard_puzzle)
	status = solver.solve_puzzle()
	if status == 'Optimal':
		solver.write_solution_to_text('solution.txt')
	else:
		print('No solution found')
