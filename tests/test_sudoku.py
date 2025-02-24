import pytest

import sudoku

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
hard_puzzle_soln = [(0, 0, 5), (0, 1, 3), (0, 2, 4), (0, 3, 6), (0, 4, 7), (0, 5, 8),
					(0, 6, 9), (0, 7, 1), (0, 8, 2), (1, 0, 6), (1, 1, 7), (1, 2, 2),
					(1, 3, 1), (1, 4, 9), (1, 5, 5), (1, 6, 3), (1, 7, 4), (1, 8, 8),
					(2, 0, 1), (2, 1, 9), (2, 2, 8), (2, 3, 3), (2, 4, 4), (2, 5, 2),
					(2, 6, 5), (2, 7, 6), (2, 8, 7), (3, 0, 8), (3, 1, 5), (3, 2, 9),
					(3, 3, 7), (3, 4, 6), (3, 5, 1), (3, 6, 4), (3, 7, 2), (3, 8, 3),
					(4, 0, 4), (4, 1, 2), (4, 2, 6), (4, 3, 8), (4, 4, 5), (4, 5, 3),
					(4, 6, 7), (4, 7, 9), (4, 8, 1), (5, 0, 7), (5, 1, 1), (5, 2, 3),
					(5, 3, 9), (5, 4, 2), (5, 5, 4), (5, 6, 8), (5, 7, 5), (5, 8, 6),
					(6, 0, 9), (6, 1, 6), (6, 2, 1), (6, 3, 5), (6, 4, 3), (6, 5, 7),
					(6, 6, 2), (6, 7, 8), (6, 8, 4), (7, 0, 2), (7, 1, 8), (7, 2, 7),
					(7, 3, 4), (7, 4, 1), (7, 5, 9), (7, 6, 6), (7, 7, 3), (7, 8, 5),
					(8, 0, 3), (8, 1, 4), (8, 2, 5), (8, 3, 2), (8, 4, 8), (8, 5, 6),
					(8, 6, 1), (8, 7, 7), (8, 8, 9)]

invalid_puzzle = [(0, 0, 1),
				  (0, 1, 1)]


@pytest.fixture
def set_up_sudoku_problem():
	return sudoku.Solver()


@pytest.mark.parametrize('puzzle,solution', [(hard_puzzle, hard_puzzle_soln)])
def test_solvable_puzzle(set_up_sudoku_problem, puzzle, solution):
	solver = set_up_sudoku_problem
	solver.set_starting_cells(puzzle)
	status = solver.solve_puzzle()
	proposed_solution = solver.parse_solution()
	assert status == 'Optimal'
	assert proposed_solution == solution


@pytest.mark.parametrize('invalid_grid', [invalid_puzzle])
def test_invalid_puzzle(set_up_sudoku_problem, invalid_grid):
	solver = set_up_sudoku_problem
	solver.set_starting_cells(invalid_grid)
	status = solver.solve_puzzle()
	assert status != 'Optimal'


def test_empty_puzzle(set_up_sudoku_problem):
	solver = set_up_sudoku_problem
	solver.set_starting_cells([])
	status = solver.solve_puzzle()
	assert status == 'Optimal'
