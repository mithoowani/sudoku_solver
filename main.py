"""
A terminal user interface (TUI) to solve 9x9 Sudoku puzzles
"""

from sudoku import Solver
from time import localtime, strftime
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Digits, Footer, Static
from textual.containers import Container
from textual import events
from textual.binding import Binding


class Cell(Digits, can_focus=True):
	"""An individual Sudoku number from 1-9; "x" marks an empty cell,
	every cell has an ID in the form '_row_col'"""

	# All cells start off empty
	output = reactive('x')

	BINDINGS = [('k', 'increment_output(1)', 'Increment'),
				('j', 'increment_output(-1)', 'Decrement'),
				('x', 'clear', 'Clear Cell')]

	def watch_output(self) -> None:
		self.update(f'{self.output}')

	def on_key(self, event: events.Key):
		if event.key.isdigit():
			if int(event.key) > 0:
				self.output = int(event.key)
		elif event.key == 'k':  # increment
			if self.output == 'x':
				self.output = 1
			elif self.output < 9:
				self.output += 1
			else:
				self.action_clear()
		elif event.key == 'j':  # decrement
			if self.output == 'x':
				self.output = 9
			elif self.output > 1:
				self.output -= 1
			else:
				self.action_clear()

	def action_clear(self) -> None:
		self.output = 'x'


class Box(Container):
	"""3 x 3 box of Sudoku digits"""

	def compose(self) -> ComposeResult:
		for i in range(9):
			box_num = int(self.id[1:])  # boxes are numbered 0 through 8

			# creates an identifier for each cell in the string format '_row_col'
			row = box_num // 3 * 3 + (i // 3)
			col = box_num % 3 * 3 + (i % 3)
			cell_id = f'_{row}_{col}'

			yield Cell(id=cell_id)


class SudokuApp(App):
	"""A screen representing a 9 x 9 Sudoku grid"""

	CSS_PATH = 'layout.tcss'

	BINDINGS = [('X', 'clear_all', 'Clear All'),
				('s', 'solve', 'Solve'),
				Binding('right', 'focus_next_digit', 'Focus Next Digit', show=False),
				Binding('left', 'focus_prev_digit', 'Focus Prev Digit', show=False),
				Binding('up', 'focus_up_digit', 'Focus Up Digit', show=False),
				Binding('down', 'focus_down_digit', 'Focus Down Digit', show=False)]

	def compose(self) -> ComposeResult:

		# the main grid is composed of nine 3x3 boxes
		with Container(id='main_grid'):
			for box_num in range(9):
				yield Box(id=f'_{box_num}')

		# 1-line logger at the bottom of the app
		self.logger = Static(id='logger')
		yield self.logger

		yield Footer()

	def action_clear_all(self) -> None:
		"""Clears the whole grid and updates log"""
		for cell in self.query(Cell):
			cell.action_clear()

		self.display_message('Cleared grid')

	def action_focus_next_digit(self) -> None:
		"""Move focus to digit right of the current one"""
		row, col = self.get_cell_row_col(self.screen.focused)

		if col < 8:
			next_button = self.query_one(f'#_{row}_{col + 1}')
			self.screen.set_focus(next_button)

		elif row < 8:
			next_button = self.query_one(f'#_{row + 1}_{0}')
			self.screen.set_focus(next_button)

	def action_focus_prev_digit(self) -> None:
		"""Move focus to digit left of the current one"""
		row, col = self.get_cell_row_col(self.screen.focused)

		if col > 0:
			next_button = self.query_one(f'#_{row}_{col - 1}')
			self.screen.set_focus(next_button)

		elif row > 0:
			next_button = self.query_one(f'#_{row - 1}_{8}')
			self.screen.set_focus(next_button)

	def action_focus_up_digit(self) -> None:
		"""Move focus to digit directly above the current one"""
		row, col = self.get_cell_row_col(self.screen.focused)

		if row > 0:
			next_button = self.query_one(f'#_{row - 1}_{col}')
			self.screen.set_focus(next_button)

	def action_focus_down_digit(self) -> None:
		"""Move focus to digit directly below the current one"""
		row, col = self.get_cell_row_col(self.screen.focused)

		if row < 8:
			next_button = self.query_one(f'#_{row + 1}_{col}')
			self.screen.set_focus(next_button)

	def display_message(self, message: str) -> None:
		"""Displays a timestamped message in the logger"""
		current_time = strftime("%H:%M:%S", localtime())
		self.logger.update(f'{current_time}: {message}')

	def action_solve(self) -> None:
		"""Solves the Sudoku puzzle and displays the result on the screen"""
		parsed_grid = self.parse_grid()
		solution = self.get_solution(parsed_grid)
		self.display_solution(solution)

	def parse_grid(self) -> list[tuple[int, int, int]]:
		"""Parses the grid into the data structure used by the solver, which is of the form [(row, col, value)...]"""
		grid = []
		for cell in self.query(Cell):
			row, col = self.get_cell_row_col(cell)
			val = 0 if cell.output == 'x' else int(cell.output)
			grid.append((row, col, val))
		return grid

	@staticmethod
	def get_solution(puzzle: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
		"""Returns the puzzle's solution"""
		solution = None
		solver = Solver(puzzle)
		status = solver.solve_puzzle()
		if status == 'Optimal':
			solution = solver.parse_solution()
		return solution

	def display_solution(self, solution):
		"""Displays the puzzle's solution on the grid"""
		if not solution:
			self.display_message('Solution not found')
		else:
			for row, col, val in solution:
				self.query_one(f'#_{row}_{col}').output = val
			self.display_message('Solution found')

	@staticmethod
	def get_cell_row_col(cell: Cell) -> (int, int):
		"""Returns the row, col of the currently focused cell. The ID's of cells follow the format '_row_col'"""
		return int(cell.id[1]), int(cell.id[3])


if __name__ == '__main__':
	app = SudokuApp()
	app.run()
