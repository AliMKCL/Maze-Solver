import maze as Maze
import runner as Runner
import copy
import os

def shortest_path(maze, starting: tuple[int, int]=None, goal: tuple[int, int]=None) -> list[tuple[int, int]]:
    if starting == None:
        starting = (0, 0)

    if goal == None:
        goal = (int(((len(maze)-1)/2-1)), (int((len(maze[0])-1)/2-1)))

    original_maze = copy.deepcopy(maze)

    visited_nodes = []  #Store values with count so that if new runners with same or more counts access same spot it wont search there
    marked_maze = [[999 for i in range(Maze.get_dimensions(maze)[0])] for j in range(Maze.get_dimensions(maze)[1])]
    count = 0
    temp_runners = []

    current_location = starting
    runner = [current_location[0], current_location[1], "E"]
    decision = Runner.sense_walls(runner, maze)

    #If initially the runner is facing a dead end, change runner direction.
    if decision.count(True) == 3:
        runner[2] = "N"

    #This part is for the special case that when a starting position not 0,0 is inputted, behind the initial direction is also a path.
    runner2 = [runner[0], runner[1], runner[2]]
    if runner[2] == "N":
        runner2[2] = "S"
        decision = Runner.sense_walls(runner2, maze)
        if decision[1] == False:
            #The 4th parameter is to determine that this is behind the initial starting
            temp_runners.append([runner2, (True, False, True), 0, 0])
    elif runner[2] == "S":
        runner2[2] = "N"
        decision = Runner.sense_walls(runner2, maze)
        if decision[1] == False:
            temp_runners.append([runner2, (True, False, True), 0, 0])
    elif runner[2] == "W":
        runner2[2] = "E"
        decision = Runner.sense_walls(runner2, maze)
        if decision[1] == False:
            temp_runners.append([runner2, (True, False, True), 0, 0])
    elif runner[2] == "E":
        runner2[2] = "W"
        decision = Runner.sense_walls(runner2, maze)
        if decision[1] == False:
            temp_runners.append([runner2, (True, False, True), 0, 0])

    goal_reversed = (goal[1], goal[0])
    flag = 0
    #goal_reversed stops the algorithm when the goal location in the maze is reached. In order to mark every location in the maze, the part after the and can be removed.
    while len(visited_nodes) != (Maze.get_dimensions(maze)[0] * Maze.get_dimensions(maze)[1]) and current_location != goal_reversed:
        
        

        #Marks visited locations with a count number. Final number on it is the shortest length path to it
        if count < marked_maze[len(marked_maze)-1-current_location[1]][current_location[0]] and flag == 0:
            marked_maze[len(marked_maze)-1-current_location[1]][current_location[0]] = count
        count +=1


        if current_location not in visited_nodes:
            visited_nodes.append(current_location)  #This will be needed to check if the entirety of the maze is scanned before finishing the run

        #This flag is for printing the marked maze in the very end, thats why later flag is set to 1 in the loop
        if flag == 0:
            decision = Runner.sense_walls(runner, maze)
        flag = 0
        
        #If a runner segment hits a dead end, continue from the other path where it split from. Stack is used to continue from left off
        if decision.count(False) == 0:

            if len(temp_runners) == 0:
                if count < marked_maze[len(marked_maze)-1-current_location[1]][current_location[0]] and flag == 0:
                    marked_maze[len(marked_maze)-1-current_location[1]][current_location[0]] = count

            else:
                paused_runner = temp_runners.pop()
                runner = paused_runner[0]

                #This decision is used for scanning the maze
                if  flag == 0 and len(paused_runner) == 3:
                    decision = Runner.sense_walls(runner, maze)
                
                elif len(paused_runner)==4:
                    decision = paused_runner[1]
                    

                flag = 0
            

                count = paused_runner[2]
                #This flag is to prevent it printing the maze values twice
                flag = 1

                direction = runner[2]
                #Add walls to block off already explored useless paths, added wall in order to turn when returned to split with move()
                #You can delete the added walls by storing its data temporarly and later checking a flag condition and deleting wall
                if decision ==  (False, False, True) or decision == (False, True, False):
                    if direction == "N":
                        Maze.add_vertical_wall(maze, runner[1], runner[0])
                    elif direction == "S":
                        Maze.add_vertical_wall(maze, runner[1], runner[0]+1)
                    elif direction == "W":
                        Maze.add_horizontal_wall(maze, runner[0], runner[1])
                    elif direction == "E":
                        Maze.add_horizontal_wall(maze, runner[0], runner[1]+1)
                    decision = Runner.sense_walls(runner, maze)
                
                #This one is for the case when there is also a path right behind the initial spot.
                elif decision == (True, False, True):
                    if direction == "N":
                        Maze.add_vertical_wall(maze, runner[1], runner[0]+1)
                    elif direction == "S":
                        Maze.add_vertical_wall(maze, runner[1], runner[0])
                    elif direction == "W":
                        Maze.add_horizontal_wall(maze, runner[0], runner[1]+1)
                    elif direction == "E":
                        Maze.add_horizontal_wall(maze, runner[0], runner[1])
                    decision = Runner.sense_walls(runner, maze)


                elif decision == (True, False, False):
                    if direction == "N":
                        Maze.add_horizontal_wall(maze, runner[0], runner[1]+1)
                    elif direction == "S":
                        Maze.add_horizontal_wall(maze, runner[0], runner[1])
                    elif direction == "W":
                        Maze.add_vertical_wall(maze, runner[1], runner[0])
                    elif direction == "E":
                        Maze.add_vertical_wall(maze, runner[1], runner[0]+1)
                    decision = Runner.sense_walls(runner, maze)
                

                #If road splits into 3, add paused runner back and continue from 1 right turn (front). On next pop it shows road splits into 2 not 3
                elif (decision == (False, False, False)):
                    #Add wall to the left
                    if direction == "N":
                        Maze.add_vertical_wall(maze, runner[1], runner[0])
                    elif direction == "S":
                        Maze.add_vertical_wall(maze, runner[1], runner[0]+1)
                    elif direction == "W":
                        Maze.add_horizontal_wall(maze, runner[0], runner[1])
                    elif direction == "E":
                        Maze.add_horizontal_wall(maze, runner[0], runner[1]+1)
                    
                    decision = Runner.sense_walls(runner, maze)
                    temp_runners.append([runner.copy(), decision, count]) #not count-1 because count was already count-1 when it first entered the 3 split


        #If there is only 1 way to go
        elif decision.count(False) == 1:
            runner = Runner.move(runner, maze)[0]
            current_location = (runner[0], runner[1])

        #If there are 2/3 ways to go/if path splits into 2/3
        elif decision.count(False) == 2 or decision.count(False) == 3:
            temp_runners.append([runner.copy(), decision, count-1])  
            runner = Runner.move(runner, maze)[0]
            current_location = (runner[0], runner[1])

    if count < marked_maze[len(marked_maze)-1-current_location[1]][current_location[0]] and flag == 0:
        marked_maze[len(marked_maze)-1-current_location[1]][current_location[0]] = count

    #Restores the maze to its original form before backtracking from goal, since walls were added in the process
    a = 0
    b = 0
    while b < len(maze):
        a = 0
        while a < len(maze[0]):
            if original_maze[b][a] != maze[b][a]:
                maze[b][a] = "."
            a+=1
        b+=1

    location = goal
    path = []
    path.append(location)
    location_mark = 999
    initial = 1
    looptime=0
    starting = (starting[1], starting[0])

    #Main backtracking loop that goes from goal to starting according to the shortest path by reading each node's marks.
    while location != starting:
        looptime+=1
        if initial == 1:
            location_mark = 999
        else:
            location_mark = marked_maze[len(marked_maze)-1-location[0]][location[1]]
        initial = 0
        
        #If there isn't a wall above and the proximity mark of above node is less than the current node
        if maze[len(maze)-1-location[0]*2-2][location[1]*2+1] != "#" and marked_maze[len(marked_maze)-1-location[0]-1][location[1]] < location_mark:
            location = (location[0]+1, location[1])
            path.append(location)

        #If there isn't a wall below and the proximity mark of below node is less than the current node
        elif maze[len(maze)-1-location[0]*2][location[1]*2+1] != "#" and marked_maze[len(marked_maze)-1-location[0]+1][location[1]] < location_mark:
            location = (location[0]-1, location[1])
            path.append(location)

        #If there isn't a wall to the left and the proximity mark of the left node is less than the current node
        elif maze[len(maze)-1-location[0]*2-1][location[1]*2] != "#" and marked_maze[len(marked_maze)-1-location[0]][location[1]-1] < location_mark:
            location = (location[0], location[1]-1)
            path.append(location)
        
        #If there isn't a wall to the right and the proximity mark of the right node is less than the current node
        elif maze[len(maze)-1-location[0]*2-1][location[1]*2+2] != "#" and marked_maze[len(marked_maze)-1-location[0]][location[1]+1] < location_mark:
            location = (location[0], location[1]+1)
            path.append(location)
        

    
    
    #If same value is in path, remove the values between when the spot is seen twice and one of the values. This can happen when a starting spot is chosen to some specific spots.
    visited_result = []
    second_index = 0
    i = 0
    while i < len(path):
        if path[i] not in visited_result:
            visited_result.append((path[i]))
        else:
            second_index = i    
            distance = second_index - visited_result.index(path[i])
            d = 0
            while d < distance:
                path.pop(0)
                d+=1
        i+=1
    

    path.reverse()
    path = [(y,x) for x,y in path]
    return path

def maze_reader(maze_file: str):
    try:
        with open(maze_file, "r") as mazefile:
            maze = mazefile.readlines()
    except:
        raise IOError
    #Deletes the newlines from maze
    i = 0
    while i < len(maze):
        if len(maze[i]) > len(maze[len(maze)-1]):
            maze[i] = maze[i][:-1]
        i+=1

    #Changes maze from string type to an array
    a = 0
    b = 0
    arr_maze = [["" for i in range(len(maze[0]))] for j in range(len(maze))]
    while a < len(maze):
        while b < len(maze[0]):
            arr_maze[a][b] = maze[a][b:b+1]
            b+=1
        b=0
        a+=1

    #Checks if any of the borders of the maze are missing
    i = 0
    while i < len(maze):
        if maze[i][0] != "#" or maze[i][len(maze[0])-1] != "#":
            raise ValueError
        i+=1
    i = 0
    while i < len(maze[0]):
        if maze[0][i] != "#" or maze[len(maze)-1][i] != "#":
            raise ValueError
        i+=1
    
    j = 0
    i=0
    column_sizes = []
    row_sizes = []
    while i < len(maze):
        while j < len(maze[0]):
            if maze[i][j] not in ".#":
                raise ValueError
            j+=1
        column_sizes.append(j)
        row_sizes.append(len(maze[i]))
        j=0
        i+=1

    for i in range(len(column_sizes)-1):
        if column_sizes[i+1] != column_sizes[i]:
            raise ValueError
    
    for i in range(len(row_sizes)-1):
        if row_sizes[i+1] != row_sizes[i]:
            raise ValueError

    return arr_maze



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser() 

    parser.add_argument(
    "--starting", type=str,                
    required=False, help="The starting position, e.g., '2,1'"     
    )

    parser.add_argument(
    "--goal", type=str,                
    required=False, help="The goal position, e.g., '4,5'"     
    )

    parser.add_argument(
    "--maze", type=str,                 
    required=True, help="The name of the maze file, e.g., maze1.mz"     
    )

    args = parser.parse_args()
    if args.starting is not None:
        starting = args.starting.split(",")
        start_x = int(starting[0])
        start_y = int(starting[1])
        starting = (start_x, start_y)
    else:
        starting = None

    if args.goal is not None:
        goal = args.goal.split(",")
        goal_x = int(goal[0])
        goal_y = int(goal[1])
        goal = (goal_y, goal_x)
    else:
        goal = None

    maze = maze_reader(args.maze)
    shortest_result = shortest_path(maze, starting, goal)
    print(shortest_result)





    if starting == None:
        path = Runner.explore([0, 0, "N"], maze, goal)
    else:
        path = Runner.explore([starting[0], starting[1], "N"], maze, goal)


    header = "Step,x-coordinate,y-coordinate,Actions\n"
    with open("exploration.csv", "w") as file:
        file.write(header)
        index = 0
        direction = "N"
        pos = []
        if starting == None:
            position = (0,0)
        else:
            position = starting
        pos.append(position)
        while index < len(path):
            
            #All of these determine the position of the runner in the explore function based on the initial direction and turn the runner makes.
            if path[index] == "F" and direction == "N":
                position = (position[0], position[1]+1)
                pos.append(position)
            elif path[index] == "RF" and direction == "N":
                direction = "E"
                position = (position[0]+1, position[1])
                pos.append(position)
            elif path[index] == "LF" and direction == "N":
                direction = "W"
                position = (position[0]-1, position[1])
                pos.append(position)
            elif path[index] == "RRF" and direction == "N":
                direction = "S"
                position = (position[0], position[1]-1)
                pos.append(position)

            elif path[index] == "F" and direction == "S":
                position = (position[0], position[1]-1)
                pos.append(position)
            elif path[index] == "RF" and direction == "S":
                direction = "W"
                position = (position[0]-1, position[1])
                pos.append(position)
            elif path[index] == "LF" and direction == "S":
                direction = "E"
                position = (position[0]+1, position[1])
                pos.append(position)
            elif path[index] == "RRF" and direction == "S":
                direction = "N"
                position = (position[0], position[1]+1)
                pos.append(position)

            elif path[index] == "F" and direction == "W":
                position = (position[0]-1, position[1])
                pos.append(position)
            elif path[index] == "RF" and direction == "W":
                direction = "N"
                position = (position[0], position[1]+1)
                pos.append(position)
            elif path[index] == "LF" and direction == "W":
                direction = "S"
                position = (position[0], position[1]-1)
                pos.append(position)
            elif path[index] == "RRF" and direction == "W":
                direction = "E"
                position = (position[0]+1, position[1])
                pos.append(position)

            elif path[index] == "F" and direction == "E":
                position = (position[0]+1, position[1])
                pos.append(position)
            elif path[index] == "RF" and direction == "E":
                direction = "S"
                position = (position[0], position[1]-1)
                pos.append(position)
            elif path[index] == "LF" and direction == "E":
                direction = "N"
                position = (position[0], position[1]+1)
                pos.append(position)
            elif path[index] == "RRF" and direction == "E":
                direction = "W"
                position = (position[0]-1, position[1])
                pos.append(position)
            

            file.write(f"{index+1}, {pos[index][0]}, {pos[index][1]}, {path[index]}\n")
            index+=1
    
    with open("statistics.txt", "w") as file:
        name = os.path.basename(f"{args.maze}")
        name = name.split("'")[0]              
        file.write(f"{name}\n")
        score = (len(path))/4 + len(shortest_result)
        file.write(f"{score}\n")
        file.write(f"{len(path)}\n")
        file.write(f"{shortest_result}\n")
        file.write(f"{len(shortest_result)}")





