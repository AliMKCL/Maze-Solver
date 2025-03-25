from maze import create_maze, add_horizontal_wall, add_vertical_wall  # type: ignore
from maze_runner import shortest_path  # type: ignore



maze = create_maze(11, 5)
maze = add_horizontal_wall(maze, 0, 1)
maze = add_vertical_wall(maze, 1, 1)
path = shortest_path(maze)
assert path[0] == (0, 0)
assert path[-1] == (10, 4)
prefix = []
for location in path:
    assert location not in prefix, f"{location} is repeated"
    prefix.append(location)





