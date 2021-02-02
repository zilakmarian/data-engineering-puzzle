import concurrent.futures
import copy
import logging
import threading
import os
from typing import List, Dict, Union, Tuple, Set

PUZZLE_INPUT_PATH = os.path.join("puzzle", "puzzle_input.txt")
STARTING_VARIANT_LENGTH_MINIMUM = 5


class PuzzleVariants:
    def __init__(self):
        self.variants = set()
        self._lock = threading.Lock()

    def variant_exists(self, variant: List[int]) -> bool:
        """Check if the variant already exists."""
        with self._lock:
            return tuple(variant) in self.variants

    def insert(self, variant: List[int]) -> None:
        """Insert variant into the found variants."""
        with self._lock:
            self.variants.add(tuple(variant))

    def reset(self) -> None:
        """Reset the current variants."""
        with self._lock:
            self.variants = set()


VARIANTS = PuzzleVariants()


class PuzzleInput:
    def __init__(self, puzzle_input_path=PUZZLE_INPUT_PATH):
        self.puzzle_input_path = puzzle_input_path
        self.data = None

    def _load_validate_puzzle_input(self) -> List[int]:
        """Load and validate puzzle input."""
        puzzle_input = []
        with open(self.puzzle_input_path) as f:
            try:
                puzzle_input = [int(line) for line in f]
            except ValueError as exc:
                raise ValueError("All items in puzzle must be integers") from exc
        if not puzzle_input:
            raise ValueError("Empty input")
        return puzzle_input

    def _sort_puzzle_input(self, puzzle_input: List[int]) -> List[int]:
        """Sort given sequence in ascending order."""
        return sorted(puzzle_input)

    def load(self) -> None:
        """Load puzzle input, validate it and store it."""
        self.data = self._sort_puzzle_input(self._load_validate_puzzle_input())
        logging.info("Puzzle input: %s ", self.data)


def _find_next_values(variant: List[int], remaining_values: List[int]) -> List[Dict[str, Union[int, List[int]]]]:
    """Find the next values that will be added to the current variant."""
    current_value = variant[-1]
    next_values = []
    for remaining_value in remaining_values:
        if remaining_value - current_value > 3:
            break
        if 1 <= remaining_value - current_value <= 3:
            next_values.append({"next_value": remaining_value,
                                "remaining_values": [item for item in remaining_values if item > remaining_value]})
    return next_values


def _prepare_compute_variants(variant: List[int], next_values: List[Dict[str, int]]) -> List[Tuple[List[int], int]]:
    """Prepare arguments for next recursive calls of compute_variant function."""
    arguments = []
    for next_value in next_values:
        new_variant = copy.deepcopy(variant)
        new_variant.append(next_value["next_value"])
        arguments.append((new_variant, next_value["remaining_values"]))
    return arguments


def compute_variant(variant: List[int], remaining_values: List[int]):
    """Compute recursively all variants that follow up from the given variant."""
    global VARIANTS
    if not remaining_values or all([remaining_value <= variant[-1] for remaining_value in remaining_values]):
        if not VARIANTS.variant_exists(variant):
            VARIANTS.insert(variant)  # set() contains only unique items
            if len(VARIANTS.variants) % 10000 == 0:
                logging.info("Found %d variants", len(VARIANTS.variants))
        return

    next_values = _find_next_values(variant, remaining_values)
    for argument in _prepare_compute_variants(variant, next_values):
        compute_variant(*argument)


class PuzzleSolver:
    def __init__(self, puzzle_input: List[int], starting_variant_length=None) -> None:
        self.puzzle_input = puzzle_input
        self.starting_variant_max_length = self._compute_starting_variant_length() if starting_variant_length is None else starting_variant_length

    def _compute_starting_variant_length(self) -> int:
        """
        Compute the ideal length of starting variants.

        Variants are computed in multiple threads and the amount of threads is determined by the amount of starting variants.
        To generate starting variants, slice from input is required. The ideal slice size is computed here.
        """
        starting_variants_length = int(len(self.puzzle_input) / 10)  # 1/10 of the data length, blind guess
        return starting_variants_length if starting_variants_length > STARTING_VARIANT_LENGTH_MINIMUM else STARTING_VARIANT_LENGTH_MINIMUM

    def get_result(self) -> Set[Tuple[int]]:
        """Log result."""
        logging.info("Result: %d", len(VARIANTS.variants))
        return VARIANTS.variants

    def _get_starting_variants(self) -> List[List[int]]:
        """
        Compute all variants that will be used starting variants.

        Each variant will be used as starting variant for each thread.
        """
        logging.info("Computing starting variants.")
        compute_variant([0], self.puzzle_input[:self.starting_variant_max_length])
        starting_variants = VARIANTS.variants
        VARIANTS.reset()
        return [list(starting_variant) for starting_variant in starting_variants]

    def run(self) -> None:
        """Run the puzzle solver."""
        starting_variants = self._get_starting_variants()
        logging.info("Creating threads for %d starting variants", len(starting_variants))
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(starting_variants)) as executor:
            thread_futures = []
            for index, starting_variant in enumerate(starting_variants):
                logging.info("Create and start thread %d with variant %s.", index, starting_variant)
                future = executor.submit(compute_variant, starting_variant, self.puzzle_input[self.starting_variant_max_length:])
                thread_futures.append(future)
            for thread_future in thread_futures:
                thread_future.result()  # Empty result


if __name__ == "__main__":
    puzzle_input = PuzzleInput()
    puzzle_input.load()
    puzzle_solver = PuzzleSolver(puzzle_input=puzzle_input.data)
    puzzle_solver.run()
    puzzle_solver.get_result()
