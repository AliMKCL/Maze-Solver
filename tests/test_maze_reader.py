"""
Created on Wed Nov 20 15:32:28 2024
"""

__author__ = "Son Hoang"
__copyright__ = "Copyright (c) 2024, University of Southampton"
__credits__ = ["Son Hoang"]
__licence__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Son Hoang"
__email__ = "T.S.Hoang@soton.ac.uk"
__status__ = "Prototype"

import pytest

from maze import get_dimensions, get_walls  # type: ignore
from maze_runner import maze_reader  # type: ignore


def test_maze_reader_maze1() -> None:
    maze = maze_reader("maze1.mz")
    assert get_dimensions(maze) == (2, 1)
    assert get_walls(maze, 1, 0) == (True, True, True, False)
    assert get_walls(maze, 0, 0) == (True, False, True, True)


def test_maze_reader_maze2() -> None:
    with pytest.raises(ValueError):
        maze = maze_reader("maze2.mz")
        
