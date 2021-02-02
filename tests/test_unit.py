import os
import pytest

from puzzle.puzzle import _find_next_values, _prepare_compute_variants, STARTING_VARIANT_LENGTH_MINIMUM, VARIANTS


@pytest.mark.unit
class TestPuzzleInput:
    @pytest.mark.parametrize("puzzle_input_path_valid, output", [("test_puzzle_input_valid.txt", [1, 5, 3, 2])])
    def test_load_validate_puzzle_input_valid(self, puzzle_input_instance, puzzle_input_directory_path, puzzle_input_path_valid, output):
        puzzle_input_instance.puzzle_input_path = os.path.join(puzzle_input_directory_path, puzzle_input_path_valid)
        assert puzzle_input_instance._load_validate_puzzle_input() == output

    @pytest.mark.parametrize("puzzle_input_filename_invalid", ["test_puzzle_input_invalid.txt",
                                                               "test_puzzle_input_invalid2.txt",
                                                               "test_puzzle_input_invalid3.txt",
                                                               "test_puzzle_input_invalid4.txt"])
    def test_load_validate_puzzle_input_invalid(self, puzzle_input_instance, puzzle_input_directory_path, puzzle_input_filename_invalid):
        puzzle_input_instance.puzzle_input_path = os.path.join(puzzle_input_directory_path, puzzle_input_filename_invalid)
        with pytest.raises(ValueError):
            puzzle_input_instance._load_validate_puzzle_input()

    @pytest.mark.parametrize("input,output", [([3, 2, 1], [1, 2, 3]), ([5, 2, 3], [2, 3, 5]),
                                              ([2, 5, 1, 3], [1, 2, 3, 5]), ([-1, -2, 3, 1], [-2, -1, 1, 3])])
    def test_sort_puzzle_input_valid(self, puzzle_input_instance, input, output):
        assert puzzle_input_instance._sort_puzzle_input(input) == output

    @pytest.mark.parametrize("input", [[1, 2, "a"],  None])
    def test_sort_puzzle_input_invalid(self, puzzle_input_instance, input):
        with pytest.raises(TypeError):
            puzzle_input_instance._sort_puzzle_input(input)

    @pytest.mark.parametrize("puzzle_input_path_valid, output", [("test_puzzle_input_valid.txt", [1, 2, 3, 5])])
    def test_load(self, puzzle_input_instance, puzzle_input_directory_path, puzzle_input_path_valid, output):
        puzzle_input_instance.puzzle_input_path = os.path.join(puzzle_input_directory_path, puzzle_input_path_valid)
        puzzle_input_instance.load()
        assert puzzle_input_instance.data == output


@pytest.mark.unit
class TestVariants:
    @pytest.mark.parametrize("input_variant,input_remaining_values,output", [([0], [1, 2, 3], [{"next_value": 1, "remaining_values": [2, 3]},
                                                                                               {"next_value": 2, "remaining_values": [3]},
                                                                                               {"next_value": 3, "remaining_values": []}]),
                                                                             ([1], [2, 5], [{"next_value": 2, "remaining_values": [5]}]),
                                                                             ([1, 2], [4, 5, 6], [{"next_value": 4, "remaining_values": [5, 6]},
                                                                                                  {"next_value": 5, "remaining_values": [6]}]),
                                                                             ([1, 3, 5], [8, 10], [{"next_value": 8, "remaining_values": [10]}]),
                                                                             ([1], [5, 6], [])])
    def test_find_next_values(self, input_variant, input_remaining_values, output):
        assert _find_next_values(input_variant, input_remaining_values) == output

    @pytest.mark.parametrize("input_variant,input_next_values,output", [([0], [{"next_value": 1, "remaining_values": [2, 3]},
                                                                               {"next_value": 2, "remaining_values": [3]},
                                                                               {"next_value": 3, "remaining_values": []}], [([0, 1], [2, 3]), ([0, 2], [3]), ([0, 3], [])]),
                                                                        ([1, 3, 5], [{"next_value": 8, "remaining_values": [10]}], [([1, 3, 5, 8], [10])]),
                                                                        ([1], [], [])])
    def test_prepare_compute_variants(self, input_variant, input_next_values, output):
        assert _prepare_compute_variants(input_variant, input_next_values) == output


@pytest.mark.unit
class TestPuzzleSolver:
    
    @pytest.mark.parametrize("puzzle_input,expected_length", [([1, 2, 3], STARTING_VARIANT_LENGTH_MINIMUM),
                                                              ([1], STARTING_VARIANT_LENGTH_MINIMUM),
                                                              ([], STARTING_VARIANT_LENGTH_MINIMUM),  # This is a bug
                                                              ([1] * 110, 11)])
    def test_compute_starting_variant_length(self, puzzle_solver_instance, puzzle_input, expected_length):
        puzzle_solver_instance.puzzle_input = puzzle_input
        assert puzzle_solver_instance._compute_starting_variant_length() == expected_length

    def test_get_starting_variants(self, puzzle_solver_instance):
        VARIANTS.reset()  # Reset previous runs
        puzzle_solver_instance.starting_variant_max_length = 2
        # 0 is starting point, so the max length of starting variant is starting_variant_max_length + 1
        assert puzzle_solver_instance._get_starting_variants() == [[0, 1, 2], [0, 2]]


