import pytest
from main import SudokuApp, Cell
from textual.widgets import Static


@pytest.mark.asyncio
async def test_cell_digit_changes():
	"""Tests whether the number within a cell changes as expected based on keyboard input"""
	app = SudokuApp()

	async with app.run_test() as pilot:
		# test increment (key press 'k') for cell in position 0, 0
		await pilot.press('k')
		assert app.query_one('#_0_0', Cell).output == 1

		# test entering a new digit into cell
		await pilot.press('9')
		assert app.query_one('#_0_0', Cell).output == 9

		# test decrement (key press 'j') for cell in position 0, 0
		await pilot.press('j')
		assert app.query_one('#_0_0', Cell).output == 8

		# pressing '0' should result in no change
		await pilot.press('0')
		assert app.query_one('#_0_0', Cell).output == 8

		# incrementing twice should display an 'x'
		await pilot.press('k', 'k')
		assert app.query_one('#_0_0', Cell).output == 'x'

		# set the cell to '1' then clear it
		await pilot.press('1', 'x')
		assert app.query_one('#_0_0', Cell).output == 'x'


@pytest.mark.asyncio
async def test_cell_focus():
	"""Tests whether changing focus between cells works as expected based on directional key presses"""
	app = SudokuApp()

	async with app.run_test() as pilot:
		# right arrow should shift focus from cell (0,0) to (0,1)
		await pilot.press('right')
		assert app.screen.focused == app.query_one('#_0_1', Cell)

		# down arrow should shift focus from cell (0, 1) to (1,1)
		await pilot.press('down')
		assert app.screen.focused == app.query_one('#_1_1', Cell)

		# two left arrow's shift should focus to cell (0, 8) by wrapping around screen
		await pilot.press('left', 'left')
		assert app.screen.focused == app.query_one('#_0_8', Cell)

		# a right arrow should shift focus to cell (1, 0) by wrapping around screen
		await pilot.press('right')
		assert app.screen.focused == app.query_one('#_1_0', Cell)


@pytest.mark.asyncio
async def test_all_cells_cleared():
	"""Test whether a cell is cleared after pressing 'X' key"""
	app = SudokuApp()

	async with app.run_test() as pilot:
		# set up the grid with a '1' in all cells
		for cell in app.query(Cell):
			cell.output = 1

		await pilot.press('X')
		for cell in app.query(Cell):
			assert cell.output == 'x'

		assert app.query_one('#logger', Static).renderable.endswith('Cleared grid')


@pytest.mark.asyncio
async def test_invalid_solution():
	"""Test whether the app displays a valid solution to an impossible puzzle"""
	app = SudokuApp()

	async with app.run_test() as pilot:
		# set up the grid with a '1' in all cells
		for cell in app.query(Cell):
			cell.output = 1

		await pilot.press('s')

		# check that the cells didn't change
		for cell in app.query(Cell):
			assert cell.output == 1

		assert app.query_one('#logger', Static).renderable.endswith('Solution not found')


@pytest.mark.asyncio
async def test_valid_solution():
	"""Test whether an empty grid appropriately generates a valid solution"""
	app = SudokuApp()

	async with app.run_test() as pilot:
		await pilot.press('s')
		assert app.query_one('#logger', Static).renderable.endswith('Solution found')