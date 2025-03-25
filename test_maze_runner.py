"""
Created on Wed Nov 13 15:32:28 2024
"""

__author__ = "Son Hoang"
__copyright__ = "Copyright (c) 2024, University of Southampton"
__credits__ = ["Son Hoang"]
__licence__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Son Hoang"
__email__ = "T.S.Hoang@soton.ac.uk"
__status__ = "Prototype"

from maze import create_maze, add_horizontal_wall  # type: ignore
from runner import (  # type: ignore
    create_runner,
    sense_walls,
    go_straight,
    get_x,
    get_y,
    turn,
    get_orientation,
    move,
)


def test_runner_sense_walls() -> None:
    """A Unit test for :py:func:`~runner.sense_walls`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a horizontal wall at (5, 2).

    3. Add a runner at (5, 2) facing East

    4. Assert that the runner sense no walls on the left and in the front, but
    there is a wall on the right.
    """
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 5, 2)
    runner = create_runner(5, 2, "E")
    assert sense_walls(runner, maze) == (False, False, True)


def test_runner_go_straight() -> None:
    """A Unit test for :py:func:`~runner.go_straight`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a horizontal wall at (5, 2).

    3. Add a runner at (5, 2) facing East

    4. Let the runner go straight

    4. Assert that the runner is at (6, 2)
    """
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 5, 2)
    runner = create_runner(5, 2, "E")
    runner = go_straight(runner, maze)
    assert get_x(runner) == 6
    assert get_y(runner) == 2


def test_move() -> None:
    """A Unit test for :py:func:`~runner.move`

    Below is the test sequence:

    1. Create a maze of size (11, 5).

    2. Add a horizontal wall at (5, 2).

    3. Add a runner at (5, 2) facing South (toward the wall)

    4. Let the runner moves and get the (new) runner and the actions.

    5. Assert that the new runner is at one of four locations (5, 3), (5, 1),
    (4, 2), (6, 2).

    6. Create a test runner at (5, 2) facing South (toward the wall).

    7. Replay the actions with the test runner. Rely on go_straight() method to
    check if the runner hits the wall.

    8. Assert that the test runner is the same as the runner after the replay.
    """
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 5, 2)
    runner = create_runner(5, 2, "S")
    runner, actions = move(runner, maze)

    test_runner = create_runner(5, 2, "S")
    assert (get_x(runner), get_y(runner)) in [
        (5, 3),
        (5, 1),
        (4, 2),
        (6, 2),
    ], f"Runner moves to far to {(get_x(runner), get_y(runner))}"

    for action in actions:
        if action == "L":
            test_runner = turn(test_runner, "Left")
        elif action == "R":
            test_runner = turn(test_runner, "Right")
        elif action == "F":
            test_runner = go_straight(test_runner, maze)
        else:
            assert False, f"Unexpected action {action}" #This one is failing #Action = Sequence

    assert get_x(runner) == get_x(test_runner), "Incorrect x-coordinate for the runner"
    assert get_y(runner) == get_y(test_runner), "Incorrect y-coordinate for the runner"
    assert get_orientation(runner) == get_orientation(test_runner), "Incorrect orientation for the runner"


def test_explore() -> None:
    """
    The test for :py:func:~runner.explore should be similar to test_move() above
    (i.e., replaying the action to see if a test runner can follow the action to
    get to the target destination. This will left as an exercise for any keen
    testers.
    """
    pass
