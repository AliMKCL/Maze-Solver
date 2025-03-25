import maze as Maze
import maze_runner as mr
import time

def create_runner(x: int=0, y: int=0, orientation: str="N"):
    runner = [x, y, orientation]
    return runner

def get_x(runner:list):
    return runner[0]

def get_y(runner:list):
    return runner[1]

def get_orientation(runner):
    return runner[2]

def turn(runner, direction:str):
    directions = ["N", "E", "S", "W"]
    if direction.lower() == "right":
        if get_orientation(runner) == "W":
            runner[2] = "N"
        else:
            runner[2] = directions[directions.index(f"{get_orientation(runner)}")+1]
    elif direction.lower()=="left":
        if get_orientation(runner) == "N":
            runner[2] = "W"
        else:
            runner[2] = directions[directions.index(f"{get_orientation(runner)}")-1]
    return runner

def forward(runner):
    if get_orientation(runner) == "N":
        runner[1] +=1
    elif get_orientation(runner) == "S":
        runner[1] -=1
    elif get_orientation(runner) == "W":
        runner[0] -=1
    elif get_orientation(runner) == "E":
        runner[0] +=1
    return runner

def sense_walls(runner, maze) -> tuple[bool, bool, bool]:
    left = False
    front = False
    right = False
    direction = get_orientation(runner)
    if direction == "N":
        if maze[len(maze)-1-(get_y(runner)*2+2)][get_x(runner)*2+1] == "#":
            front = True
        if maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2] == "#":
            left = True
        if maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2+2] == "#":
            right = True

    elif direction == "S":
        if maze[len(maze)-1-(get_y(runner)*2)][get_x(runner)*2+1] == "#":
            front = True
        if maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2+2] == "#":
            left = True
        if maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2] == "#":
            right = True

    elif direction == "W":
        if maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2] == "#":
            front = True
        if maze[len(maze)-1-(get_y(runner)*2)][get_x(runner)*2+1] == "#":
            left = True
        if maze[len(maze)-1-(get_y(runner)*2+2)][get_x(runner)*2+1] == "#":
            right = True

    elif direction == "E":
        if maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2+2] == "#":
            front = True
        if maze[len(maze)-1-(get_y(runner)*2+2)][get_x(runner)*2+1] == "#":
            left = True
        if maze[len(maze)-1-(get_y(runner)*2)][get_x(runner)*2+1] == "#":
            right = True
        
    return (left, front, right)

def go_straight(runner, maze):
    try:
        if sense_walls(runner, maze)[1] == False:
            forward(runner)
        else:
            raise ValueError
    except IndexError:
        raise ValueError

    finally:
        return runner

def move(runner, maze):
    global sequence
    sequence = ""
    options = sense_walls(runner, maze)
    if options[0] == False:
        turn(runner, "left")
        sequence = "LF"
        go_straight(runner, maze)
    elif options[1] == False:
        sequence = "F"
        go_straight(runner, maze)
    elif options[2] == False:
        turn(runner, "right")
        sequence = "RF"
        go_straight(runner, maze)
    else:
        turn(runner, "right")
        turn(runner, "right")
        sequence = "RRF"
        go_straight(runner, maze)
    return (runner, sequence)


def explore(runner, maze, goal: tuple[int, int] = None) -> list: #Removed | None before =
    target = [0]*2
    runner_location = [0]*2
    sequence = []
    #Set goal if not set previously
    if goal == None:
        goal = Maze.get_dimensions(maze)
        target[0] = goal[0]-1
        target[1] = goal[1]-1

    #Create runner_location array for easier location-target comparison
    runner_location[0] = runner[0]
    runner_location[1] = runner[1]

    while runner_location != target:
        mark_player(runner, maze)
        
        #Update runner and sequence
        result = move(runner, maze)
        runner = result[0]
        #sequence += result[1]
        sequence.append(result[1])
        
        #Update runner location
        runner_location[0] = runner[0]
        runner_location[1] = runner[1]

    #Updates in the end when runner reaches target
    if runner_location == target:
        maze[len(maze)-1-(target[1]*2+1)][target[0]*2+1] = "X"
        

    return sequence

#Show runner orientation in maze
def mark_player(runner, maze):
    direction = get_orientation(runner)
    if direction == "N":
        maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2+1] = "^"
    elif direction == "S":
        maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2+1] = "v"
    elif direction == "W":
        maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2+1] = "<"
    elif direction == "E":
        maze[len(maze)-1-(get_y(runner)*2+1)][get_x(runner)*2+1] = ">"
    return maze


    






    