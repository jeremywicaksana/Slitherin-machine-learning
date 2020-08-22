from gameobjects import GameObject
from move import Move, Direction
import math
import time

class Agent():

   

    def __init__(self, parent = None , Pos = None, directions = None): #

        self.f = 0
        self.g = 0
        self.h = 0
        self.Pos = Pos
        self.parent = parent
        self.directions = directions
        self.width = 25
        self.length = 25


 
        """" Constructor of the Agent, can be used to set up variables """

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)

        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :param head_position: (x,y) of the head of the snake. The following should always hold: board[head_position[
        0]][head_position[1]] == GameObject.SNAKE_HEAD.

        :param body_parts: the array of the locationxs of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """
        #find coordinates of food(s)
        snakeHead = (head_position[0], head_position[1])

        foods = []
        distance = []
        temp = 1000
        choiceFood = ["nothing"]
        for x in range(self.width):
            for y in range(self.length):
                if board[x][y] == GameObject.FOOD:
                    foods.append((x,y))
                    distance.append(abs(x-snakeHead[0]) + abs(y-snakeHead[1]))

        for index, item in enumerate(distance):
            if item < temp:
                temp = item
                choiceFood[0] = foods[index]


        rootNode = Agent(None, snakeHead, direction)
        foodNode = Agent(None, choiceFood[0], None)

        openList = []
        closedList = []
        #add root node to the openList
        openList.append(rootNode)

        #implements time
        program_start = time.time()

        sum = 0
        while len(openList) > 0:
            sum += 1
            #print(sum)
            now = time.time()
            currentNode = openList[0]
            currentIndex = 0

            #once body is created calculate how many body in up, down, left, right
            snakeBodyRight = 0
            snakeBodyLeft = 0
            snakeBodyUp = 0
            snakeBodyDown = 0
            areaLeftClean = snakeHead[0]*self.width
            areaRightClean = (self.width - snakeHead[0])*self.width 
            areaDownClean = (self.width - snakeHead[1])*self.width
            areaUpClean = snakeHead[1]*self.width
            for a in body_parts:
                if a[0] > snakeHead[0]: #body on the right
                    snakeBodyRight += 1
                elif a[0] < snakeHead[0]: #body on the left
                    snakeBodyLeft += 1

            for a in body_parts:    
                if a[1] > snakeHead[1]:  #body snake below head
                    snakeBodyDown += 1
                elif a[1] < snakeHead[1]: #body snake above head
                    snakeBodyUp += 1

            # areaLeftClean = areaLeftClean - snakeBodyLeft
            # areaRightClean = areaRightClean - snakeBodyRight
            # areaDownClean = areaDownClean - snakeBodyDown
            # areaUpClean = areaUpClean - snakeBodyUp
            areaLeftClean = (areaLeftClean - snakeBodyLeft)/(areaLeftClean + 1)
            areaRightClean = (areaRightClean - snakeBodyRight)/(areaRightClean+1)
            areaDownClean = (areaDownClean - snakeBodyDown)/(areaDownClean+1)
            areaUpClean = (areaUpClean - snakeBodyUp)/(areaUpClean+1)
            #print("up", areaUpClean, "down", areaDownClean, "left", areaLeftClean, "right", areaRightClean)

             
            if now - program_start > 0.01 :

                move = None
                if snakeHead[1] - 1 < 0 or snakeHead[1] + 1 >= self.width or snakeHead[0] - 1 < 0 or snakeHead[0] + 1 >= self.width: # at the edges
                    if direction == Direction.NORTH:
                        if areaLeftClean > areaRightClean and snakeBodyLeft < snakeBodyRight:
                            move = Move.LEFT

                            if snakeHead[0] - 1 < 0: #if the snake besides the left edges
                                move = Move.RIGHT
                                if board[snakeHead[0] + 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] + 1][snakeHead[1]] == GameObject.WALL: #left edges and obstacles on the right
                                    move = Move.STRAIGHT
                            elif snakeHead[0] - 1 >= 0 and snakeHead[0] + 1 <self.width:
                                if board[snakeHead[0] - 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] - 1][snakeHead[1]] == GameObject.WALL:# if left is obstacles while on upper edge
                                    move = Move.RIGHT
                            elif snakeHead[0] + 1 >= self.width:
                                if board[snakeHead[0] - 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] - 1][snakeHead[1]] == GameObject.WALL: #right edges and obstacles on the left
                                    move = Move.STRAIGHT

                        else: 
                            move = Move.RIGHT

                            if snakeHead[0] - 1 < 0 and (board[snakeHead[0] + 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] + 1][snakeHead[1]] == GameObject.WALL): #if the snake besides the left edgesa and right is obstacle
                                move = Move.STRAIGHT
                            elif snakeHead[0] - 1 >= 0 and snakeHead[0] + 1 < self.width:
                                if board[snakeHead[0] + 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] + 1][snakeHead[1]] == GameObject.WALL:# if right is obstacles while on upper edge
                                    move = Move.LEFT
                            elif snakeHead[0] + 1 >= self.width:
                                move = Move.LEFT
                                if board[snakeHead[0] - 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] - 1][snakeHead[1]] == GameObject.WALL: #right edges and obstacles on the left
                                    move = Move.STRAIGHT

                    elif direction == Direction.SOUTH:
                        if areaLeftClean > areaRightClean and snakeBodyLeft < snakeBodyRight:
                            move = Move.RIGHT #go to left
                            
                            if snakeHead[0] - 1 < 0: #if the snake besides the left edges
                                move = Move.LEFT
                                if board[snakeHead[0] + 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] + 1][snakeHead[1]] == GameObject.WALL: #left edges and obstacles on the right
                                    move = Move.STRAIGHT
                            elif snakeHead[0] - 1 >= 0 and snakeHead[0] + 1 <self.width:
                                if board[snakeHead[0] - 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] - 1][snakeHead[1]] == GameObject.WALL:# if left is obstacles while on upper edge
                                    move = Move.LEFT
                            elif snakeHead[0] + 1 >= self.width:
                                if board[snakeHead[0] - 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] - 1][snakeHead[1]] == GameObject.WALL: #right edges and obstacles on the left
                                    move = Move.STRAIGHT
                        else: 
                            move = Move.LEFT
                            
                            if snakeHead[0] - 1 < 0 and (board[snakeHead[0] + 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] + 1][snakeHead[1]] == GameObject.WALL): #if the snake besides the left edgesa and right is obstacle
                                move = Move.STRAIGHT
                            elif snakeHead[0] - 1 >= 0 and snakeHead[0] + 1 < self.width:
                                if board[snakeHead[0] + 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] + 1][snakeHead[1]] == GameObject.WALL:# if right is obstacles while on upper edge
                                    move = Move.RIGHT
                            elif snakeHead[0] + 1 >= self.width:
                                move = Move.RIGHT
                                if board[snakeHead[0] - 1][snakeHead[1]] == GameObject.SNAKE_BODY or board[snakeHead[0] - 1][snakeHead[1]] == GameObject.WALL: #right edges and obstacles on the left
                                    move = Move.STRAIGHT

                    elif direction == Direction.EAST:
                        if areaDownClean > areaUpClean and snakeBodyDown < snakeBodyUp:
                            move = Move.RIGHT
                            if snakeHead[1] - 1 < 0 and (board[snakeHead[0]][snakeHead[1] + 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] + 1] == GameObject.WALL): # if snake besides upper edgees and below is obstacle
                                move = Move.STRAIGHT
                            elif snakeHead[1] - 1 >= 0 and snakeHead[1] + 1 < self.width:
                                if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL:# if down is obstacle while on right edge
                                    move = Move.LEFT
                            elif snakeHead[1] + 1 >= self.width:
                                move = Move.LEFT
                                if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL: #down edges and obstacles on up
                                    move = Move.STRAIGHT

                        else:
                            move = Move.LEFT

                            if snakeHead[1] - 1 < 0: # if snake besides upper edgees
                                move = Move.RIGHT
                                if board[snakeHead[0]][snakeHead[1] + 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] + 1] == GameObject.WALL: #if below is obstacle
                                    move = Move.STRAIGHT
                            elif snakeHead[1] - 1 >= 0 and snakeHead[1] + 1 < self.width:
                                if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL:# if down is obstacle while on right edge
                                    move = Move.RIGHT
                            elif snakeHead[1] + 1 >= self.width:
                                if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL: #down edges and obstacles on up
                                    move = Move.STRAIGHT

                    else: #west
                        if areaDownClean > areaUpClean and snakeBodyDown < snakeBodyUp:
                            move = Move.LEFT
                            
                            if snakeHead[1] - 1 < 0 and (board[snakeHead[0]][snakeHead[1] + 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] + 1] == GameObject.WALL): # if snake besides upper edgees and below is obstacle
                                move = Move.STRAIGHT
                            elif snakeHead[1] - 1 >= 0 and snakeHead[1] + 1 < self.width:
                                if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL:# if down is obstacle while on left edge
                                    move = Move.RIGHT
                            elif snakeHead[1] + 1 >= self.width:
                                move = Move.RIGHT
                                if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL: #down edges and obstacles on up
                                    move = Move.STRAIGHT                 
                        else:
                            move = Move.RIGHT
                            
                            if snakeHead[1] - 1 < 0: # if snake besides upper edgees
                                move = Move.LEFT
                                if board[snakeHead[0]][snakeHead[1] + 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] + 1] == GameObject.WALL: #if below is obstacle
                                    move = Move.STRAIGHT
                            elif snakeHead[1] - 1 >= 0 and snakeHead[1] + 1 < self.width:
                                if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL:# if up is obstacle while on left edge
                                    move = Move.LEFT
                            elif snakeHead[1] + 1 >= self.width:
                                if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL: #down edges and obstacles on up
                                    move = Move.STRAIGHT

                else: 
                    if direction == Direction.NORTH:
                        move = Move.STRAIGHT
                        if board[snakeHead[0]][snakeHead[1] - 1] == GameObject.WALL or board[snakeHead[0]][snakeHead[1] - 1] == GameObject.SNAKE_BODY: #check if above obstacles
                            if areaRightClean > areaLeftClean and snakeBodyRight < snakeBodyLeft: #lots of body parts on left
                                if board[snakeHead[0] + 1][snakeHead[1]] ==  GameObject.EMPTY:
                                    move = Move.RIGHT
                                else:
                                    move = Move.LEFT
                            else: #if body parts on left is smaller than right
                                if board[snakeHead[0] - 1][snakeHead[1]] ==  GameObject.EMPTY:
                                    move = Move.LEFT
                                else:
                                    move = Move.RIGHT
                            
                    elif direction == Direction.SOUTH:
                        move = Move.STRAIGHT
                        if board[snakeHead[0]][snakeHead[1] + 1] == GameObject.WALL or board[snakeHead[0]][snakeHead[1] + 1] == GameObject.SNAKE_BODY: #check if belo obstacles
                            if areaRightClean > areaLeftClean and snakeBodyRight < snakeBodyLeft: #lots of body parts on left
                                if board[snakeHead[0] + 1][snakeHead[1]] ==  GameObject.EMPTY:
                                    move = Move.LEFT
                                else:
                                    move = Move.RIGHT
                            else: #if body parts on left is smaller than right
                                if board[snakeHead[0] - 1][snakeHead[1]] ==  GameObject.EMPTY:
                                    move = Move.RIGHT
                                else:
                                    move = Move.LEFT

                    elif direction == Direction.EAST:
                        move = Move.STRAIGHT
                        if board[snakeHead[0] + 1][snakeHead[1]] == GameObject.WALL or board[snakeHead[0] + 1][snakeHead[1]] == GameObject.SNAKE_BODY: #check if right obstacles
                            if areaUpClean > areaDownClean and snakeBodyUp < snakeBodyDown: #lots of body parts on below
                                if board[snakeHead[0]][snakeHead[1] - 1] ==  GameObject.EMPTY:
                                    move = Move.LEFT
                                else:
                                    move = Move.RIGHT
                            else: #if body parts on below is lower than upper
                                if board[snakeHead[0]][snakeHead[1] + 1] ==  GameObject.EMPTY:
                                    move = Move.RIGHT
                                else:
                                    move = Move.LEFT

                    else: #west
                        move = Move.STRAIGHT
                        if board[snakeHead[0] - 1][snakeHead[1]] == GameObject.WALL or board[snakeHead[0]-1][snakeHead[1]] == GameObject.SNAKE_BODY: #check if left obstacles
                            if areaUpClean > areaDownClean and snakeBodyUp < snakeBodyDown: #lots of body parts on below
                                if board[snakeHead[0]][snakeHead[1] - 1] ==  GameObject.EMPTY:
                                    move = Move.RIGHT
                                else:
                                    move = Move.LEFT
                            else: #if body parts on below is lower than upper
                                if board[snakeHead[0]][snakeHead[1] + 1] ==  GameObject.EMPTY:
                                    move = Move.LEFT
                                else:
                                    move = Move.RIGHT

                return move

                                

            for index, item in enumerate(openList):
                if item.f < currentNode.f or (item.f == currentNode.f and item.g < currentNode.g):
                    currentIndex = index
                    currentNode = item
            
            openList.pop(currentIndex)#remove current node that is calculated
            closedList.append(currentNode)#removed node in openList is moved to closedList


            if (currentNode.Pos == foodNode.Pos):
                path = []
                current = currentNode
                while current is not None:
                    path.append(current.Pos)
                    current = current.parent
                #print(path[::-1])
                move = None
                path = path[::-1]
                xAxis = path[1][0] - path[0][0]
                yAxis = path[1][1] - path[0][1]

                if(direction == Direction.NORTH):
                    if xAxis < 0 and yAxis == 0: #left
                        move = Move.LEFT 
                    elif xAxis > 0 and yAxis == 0: #right
                        move = Move.RIGHT
                    else: #yAxis < 0 #up
                        move = Move.STRAIGHT

                elif(direction == Direction.SOUTH):
                    if xAxis < 0 and yAxis == 0: #left
                        move = Move.RIGHT 
                    elif yAxis > 0 and xAxis == 0: #down
                        move = Move.STRAIGHT
                    else: #right
                        move = Move.LEFT


                elif(direction == Direction.EAST):
                    if yAxis > 0 and xAxis == 0: #down
                        move = Move.RIGHT  
                    elif xAxis > 0 and yAxis == 0: #right
                        move = Move.STRAIGHT
                    else: #yAxis < 0 #up
                        move = Move.LEFT

                else: #west
                    if xAxis < 0 and yAxis == 0: #left
                        move = Move.STRAIGHT 
                    elif yAxis > 0 and xAxis == 0: #down
                        move = Move.LEFT 
                    else: #yAxis < 0 #up
                        move = Move.RIGHT
                
                return move


            branches = []
            north = [(1,0), (-1, 0), (0,-1)] #right, left, up
            south = [(1,0), (-1, 0), (0, 1)] #rightm, left, down
            east = [(1,0), (0, 1), (0,-1)] #right, up, down
            west = [(0,1), (-1, 0), (0,-1)] #down, left, up

            if currentNode.directions == Direction.NORTH:
                for adjacent in north:
                    curDirection = None 
                    neighbor = (currentNode.Pos[0] + adjacent[0], currentNode.Pos[1] + adjacent[1])
                    
                    if neighbor[0] < 0 or neighbor[0] > (self.length - 1) or neighbor[1] < 0 or neighbor[1] > (self.length -1):
                        continue

                    if board[neighbor[0]][neighbor[1]] == GameObject.SNAKE_BODY or board[neighbor[0]][neighbor[1]] == GameObject.WALL:
                        continue

                    #check the direction of the neighbor
                    if neighbor[0] < currentNode.Pos[0] and neighbor[1] == currentNode.Pos[1]:
                        curDirection = Direction.WEST
                    elif neighbor[0] > currentNode.Pos[0] and neighbor[1] == currentNode.Pos[1]:
                        curDirection = Direction.EAST
                    else: 
                        curDirection = Direction.NORTH

                    

                    newBranch = Agent(currentNode, neighbor, curDirection)
                    branches.append(newBranch)

            elif currentNode.directions == Direction.SOUTH:
                for adjacent in south:
                    curDirection = None
                    neighbor = (currentNode.Pos[0] + adjacent[0], currentNode.Pos[1] + adjacent[1])
                    
                    if neighbor[0] < 0 or neighbor[0] > (self.length - 1) or neighbor[1] < 0 or neighbor[1] > (self.length -1):
                        continue

                    if board[neighbor[0]][neighbor[1]] == GameObject.SNAKE_BODY or board[neighbor[0]][neighbor[1]] == GameObject.WALL:
                        continue

                    #check the direction of the neighbor
                    if neighbor[0] < currentNode.Pos[0] and neighbor[1] == currentNode.Pos[1]:
                        curDirection = Direction.WEST
                    elif neighbor[0] > currentNode.Pos[0] and neighbor[1] == currentNode.Pos[1]:
                        curDirection = Direction.EAST
                    else: 
                        curDirection = Direction.SOUTH

                    newBranch = Agent(currentNode, neighbor, curDirection)
                    branches.append(newBranch)

            elif currentNode.directions ==  Direction.EAST:
                for adjacent in east:
                    curDirection = None
                    neighbor = (currentNode.Pos[0] + adjacent[0], currentNode.Pos[1] + adjacent[1])
                    
                    if neighbor[0] < 0 or neighbor[0] > (self.length - 1) or neighbor[1] < 0 or neighbor[1] > (self.length -1):
                        continue

                    if board[neighbor[0]][neighbor[1]] == GameObject.SNAKE_BODY or board[neighbor[0]][neighbor[1]] == GameObject.WALL:
                        continue

                    #check the direction of the neighbor
                    if neighbor[0] > currentNode.Pos[0] and neighbor[1] == currentNode.Pos[1]:
                        curDirection = Direction.EAST
                    elif neighbor[1] > currentNode.Pos[1] and neighbor[0] == currentNode.Pos[0]:
                        curDirection = Direction.SOUTH
                    else: 
                        curDirection = Direction.NORTH
                    newBranch = Agent(currentNode, neighbor, curDirection)
                    branches.append(newBranch)

            else: #west
                for adjacent in west:
                    curDirection = None
                    neighbor = (currentNode.Pos[0] + adjacent[0], currentNode.Pos[1] + adjacent[1])
                    
                    if neighbor[0] < 0 or neighbor[0] > (self.length - 1) or neighbor[1] < 0 or neighbor[1] > (self.length -1):
                        continue

                    if board[neighbor[0]][neighbor[1]] == GameObject.SNAKE_BODY or board[neighbor[0]][neighbor[1]] == GameObject.WALL:
                        continue

                    #check the direction of the neighbor
                    if neighbor[1] > currentNode.Pos[1] and neighbor[0] == currentNode.Pos[0]:
                        curDirection = Direction.SOUTH
                    elif neighbor[0] < currentNode.Pos[0] and neighbor[1] == currentNode.Pos[1]:
                        curDirection = Direction.WEST
                    else: 
                        curDirection = Direction.NORTH

                    newBranch = Agent(currentNode, neighbor, curDirection)
                    branches.append(newBranch)


            #get all of the child in the current branches and calculate the f/g/h
            
            for child in branches:

                child.g = currentNode.g + 1
                child.h = ((child.Pos[0] - foodNode.Pos[0]) ** 2) + ((child.Pos[1] - foodNode.Pos[1]) ** 2)
                child.f = child.g + child.h
             
                openList.append(child)
 
            
        
    def should_redraw_board(self):
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    def should_grow_on_food_collision(self):
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return True

    def on_die(self, head_position, board, score, body_parts):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.

        :param head_position: (x, y) position of the head at the moment of dying.

        :param board: two dimensional array representing the board of the game at the moment of dying. The board
        given does not include information about the snake, only the food position(s) and wall(s) are listed.

        :param score: score at the moment of dying.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.
        When the snake runs in its own body the following holds: head_position in body_parts.
        """
