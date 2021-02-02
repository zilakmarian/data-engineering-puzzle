import os
import pytest

from puzzle.puzzle import PuzzleInput, PuzzleSolver


@pytest.fixture()
def puzzle_input_directory_path():
    return "test_data"


@pytest.fixture()
def puzzle_input_valid_filepath():
    return "test_puzzle_input_valid.txt"


@pytest.fixture()
def puzzle_input_instance(puzzle_input_directory_path, puzzle_input_valid_filepath):
    puzzle_input = PuzzleInput(puzzle_input_path=os.path.join(puzzle_input_directory_path, puzzle_input_valid_filepath))
    puzzle_input.load()
    return puzzle_input


@pytest.fixture()
def puzzle_solver_instance(puzzle_input_instance):
    return PuzzleSolver(puzzle_input=puzzle_input_instance.data)
