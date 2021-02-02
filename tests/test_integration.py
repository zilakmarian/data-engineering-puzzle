import pytest


@pytest.mark.integration
class TestPuzzleSolver:
    def test_run(self, puzzle_solver_instance):
        puzzle_solver_instance.run()
        assert puzzle_solver_instance.get_result() == set([(0, 2, 3, 5), (0, 1, 3, 5), (0, 1, 2, 3, 5), (0, 2, 5), (0, 3, 5), (0, 1, 2, 5)])
