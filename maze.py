#The path to the mazes might not be correct as I put them inside the folder mazes after finishing the project
#It should work if you put the mazes in the same folder as the maze.py file

def create_maze(width=5, height=5):
    maze = [["." for i in range(width*2+1)] for j in range(height*2+1)]
    for i in range(len(maze[0])):
        maze[0][i] = "#"
        maze[len(maze)-1][i] = "#"

    for j in range(len(maze)):
        maze[j][0] = "#"
        maze[j][len(maze[0])-1] = "#"
        for x in range(len(maze[0])):
            if j%2 == 0 and x%2 == 0:
                maze[j][x] = "#"

    return maze


def add_vertical_wall(maze, y_coordinate, vertical_line):
    maze[len(maze)-1-(y_coordinate*2+1)][vertical_line*2] = "#"
    return maze

def add_horizontal_wall(maze, x_coordinate, horizontal_line):
    maze[len(maze)-1-(horizontal_line*2)][x_coordinate*2+1] = "#"
    return maze

def get_dimensions(maze) -> tuple[int, int]:
    width = int((len(maze[0])-1)/2)
    height = int((len(maze)-1)/2)
    return (width, height)

def get_walls(maze, x_coordinate: int, y_coordinate: int) -> tuple[bool, bool, bool, bool]:
    north = False
    east = False
    south = False
    west = False

    if maze[len(maze)-1 - (y_coordinate*2+1+1)][x_coordinate*2+1] == "#":# and (len(maze)-1 - (y_coordinate*2+1+1)) != 0:
        north = True
    if maze[len(maze)-1 - (y_coordinate*2+1-1)][x_coordinate*2+1] == "#":# and (len(maze)-1 - (y_coordinate*2+1+1)) != len(maze)-1:
        south = True
    if maze[len(maze)-1 - (y_coordinate*2+1)][x_coordinate*2+1+1] == "#":# and (x_coordinate*2+1+1) != len(maze[0])-1:
        east = True
    if maze[len(maze)-1 - (y_coordinate*2+1)][x_coordinate*2+1-1] == "#":# and (x_coordinate*2+1+1) != 0:
        west = True
    return(north, east, south, west)

def print_maze(maze) ->None:
    m_print = ""
    numrows = len(maze)
    i = 0
    while i < numrows:
        for j in maze[i]:
            m_print += j
        print(f"{m_print}")
        m_print=""
        i+=1









