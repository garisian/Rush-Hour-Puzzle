	#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
rushhour STATESPACE
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint

##################################################
# The search space class 'rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################


class rushhour(StateSpace):
    def __init__(self, action, gval, numColumns, numRows, vehicles, goalEntrance, goalDirection, parent = None):
        """Initialize a rushhour search state object."""
        #IMPLEMENT
        StateSpace.__init__(self, action, gval, parent)

        self.numColumns = numColumns
        self.numRows = numRows
        self.goalEntrance = goalEntrance
        self.goalDirection = goalDirection
        self.vehicles = vehicles

        self.makeBoard()          
        self.addVehicles()
        self.addGoalVeh()

    def addGoalVeh(self):
        for vehicle in self.vehicles:
            if(vehicle[4]):
                self.goalVehicle = vehicle

    def addVehicles(self):
        """Add Vehicles to the generated board"""
        for vehicle in self.vehicles:
            tempSize = vehicle[2]
            vehicleX = vehicle[1][0]
            vehicleY = vehicle[1][1]
            while(tempSize > 0):
                if(vehicle[3]):
                    self.cells[vehicleY][vehicleX] = vehicle[0]
                    if(vehicleX == self.numColumns - 1):
                        vehicleX = 0
                    else:
                        vehicleX += 1                        
                else:
                    self.cells[vehicleY][vehicleX] = vehicle[0]
                    if(vehicleY == self.numRows - 1):
                        vehicleY = 0
                    else:
                        vehicleY += 1
                tempSize -= 1
     
    def makeBoard(self):
        """Initialize a baord using the numColumns and numRows"""
        self.cells = []
        for row  in range(self.numRows):
            self.cells.append([])
            for column in range(self.numColumns):
                self.cells[row].append("")


    def successors(self):
        #IMPLEMENT
        '''Return list of rushhour objects that are the successors of the current object'''
        States = list()
        for vehicle in self.vehicles:
            #if vehicle is horizontal
            if(vehicle[3]):
                if(self.move_vehicle(vehicle,'E')):
                    States.append(self.move_vehicle(vehicle,'E'))
                if(self.move_vehicle(vehicle,'W')):
                    States.append(self.move_vehicle(vehicle,'W'))
            else:
                if(self.move_vehicle(vehicle,'N')):
                    States.append(self.move_vehicle(vehicle,'N'))
                if(self.move_vehicle(vehicle,'S')):
                    States.append(self.move_vehicle(vehicle,'S'))                
        return States
    
    def move_vehicle(self,vehicle, direction):
        '''Checks if a vehicle can be moved in that direction and if it could, returns the state. Otherwise False'''
        tempSize = vehicle[2]
        vehicleX = vehicle[1][0]
        vehicleY = vehicle[1][1]

        if(direction == 'N'):
            vehicleY -= 1
            if(vehicleY < 0):
                vehicleY = self.numRows - 1
        if(direction == 'S'):
            vehicleY += 1
            if(vehicleY >= self.numRows):
                vehicleY = 0
        if(direction == 'W'):
            vehicleX -= 1
            if(vehicleX < 0):
                vehicleX = self.numColumns - 1
        if(direction == 'E'):
            vehicleX += 1
            if(vehicleX >= self.numRows):
                vehicleX = 0
        new_vehicles = []
        #[<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
       #(self, action, gval, numColumns, numRows, vehicles, goalEntrance, goalDirection, parent = None):
        occupiedSpots = 0
        for vehicle_temp in self.vehicles:
            occupiedSpots += vehicle[2]
            if(vehicle_temp[0] == vehicle[0]):
                new_vehicles.append([vehicle[0],(vehicleX,vehicleY),vehicle[2],vehicle[3],vehicle[4]]	)
            else:
                new_vehicles.append(vehicle_temp)
        newRushHour = rushhour("move_vehicle("+vehicle[0]+", '"+direction+"')", self.gval + 1, self.numColumns, self.numRows, new_vehicles, self.goalEntrance, self.goalDirection, self)
         
        # check if new state has same number of occupied spots as current. If not, then something got overwritten and a collision 
        # occured
        newOccupiedSpots = 0
        for row in newRushHour.cells:
            for column in row:
                if(column != ""):
                    newOccupiedSpots += 1
        if(newOccupiedSpots == occupiedSpots):
            return newRushHour
        return False

    def hashable_state(self):
        #IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        return self.vehicles        

    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output.
        #Note that if you implement the "get" routines
        #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
        #properly, this function should work irrespective of how you represent
        #your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

    #Data accessor routines.

    def get_vehicle_statuses(self):
        #IMPLEMENT
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the robot (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''
        return self.vehicles

    def get_board_properties(self):
        #IMPLEMENT
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        return ((self.numColumns, self.numRows), self.goalEntrance, self.goalDirection)

#############################################
# heuristics                                #
#############################################


def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''

    return 0


def heur_min_moves(state):
    #IMPLEMENT
    '''rushhour heuristic'''
    #We want an admissible heuristic. Getting to the goal requires
    #one move for each tile of distance.
    #Since the board wraps around, there are two different
    #directions that lead to the goal.
    #NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    #1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.
    
    #print ("---------start-----'")
    goalVehicle = ""
    for vehicle in state.vehicles:
        if(vehicle[4]):
            goalVehicle = vehicle
    simpleRushHour = make_init_state((state.numColumns,state.numRows), [goalVehicle], state.goalEntrance, state.goalDirection)
    searchList = [simpleRushHour]
    visited = [] 
    while(searchList):
        combination = visited
        combination.extend(searchList)
        firstElement = searchList[0]
        searchList.remove(firstElement)
        for element in combination:
            if(element.hashable_state() == firstElement.hashable_state()):
                pass
        
        visited.append(firstElement)
        if(rushhour_goal_fn(firstElement)):
            return firstElement.gval
        successors = firstElement.successors()
        switch = 0
        for successie in successors:
            switch = 0
            for element in combination:
                if(element.hashable_state() == successie.hashable_state()):
                    switch = 1
            if(switch == 0):
                searchList.append(successie)
            
        
    #for state in simpleRushHour.successors():
    #    print(state.vehicles)
    
    #print ("---------done-----'\n\n")
    #s = simpleRushHour.move_vehicle(goalVehicle,'E')
    #print(rushhour_goal_fn(s))
    #s = s.move_vehicle(s.goalVehicle,'E')
    #print(rushhour_goal_fn(s))
    #s = s.move_vehicle(s.goalVehicle,'E')
    #print(rushhour_goal_fn(s))
    #s = s.move_vehicle(s.goalVehicle,'E')
    #print(rushhour_goal_fn(s))
    #print(s.vehicles)
    #print(goalVehicle)
    """
    print(simpleRushHour.vehicles)
    if(rushhour_goal_fn(simpleRushHour)):
        return 0
    costVal = 0
    s = simpleRushHour
    w = simpleRushHour
    print(vehicle[3])
    if(vehicle[3]):
        while(1):
            costVal += 1
            s = s.move_vehicle(goalVehicle,'E')
            w = w.move_vehicle(goalVehicle,'W')
            #print(s.vehicles)
            #print(w.vehicles)
            if(rushhour_goal_fn(s) or rushhour_goal_fn(w)):
                return costVal
    else:
        #while(1):
            costVal += 1
            s = s.move_vehicle(goalVehicle,'N')
            w = w.move_vehicle(goalVehicle,'W')
            if(rushhour_goal_fn(s) or rushhour_goal_fn(w)):
                return costVal
    """
    """
    visited = list()
    toDigestCost = list()
    toDigestObject = list()

    simpleRushHour = make_init_state((state.numColumns,state.numRows), [goalVehicle], state.goalEntrance, state.goalDirection)
    toDigestCost.append(0)
    toDigestObject.append(simpleRushHour)

    while(toDigestObject):
        cheapestObject = toDigestObject[toDigestCost.index(min(toDigestCost))]
        print(cheapestObject.vehicles)
        if(rushhour_goal_fn(cheapestObject)):
            return min(toDigestCost)
        toDigestObject.remove(cheapestObject)
        toDigestCost.remove(min(toDigestCost))
        cheapestObject.hashable_state().sort()
        visited.append(cheapestObject.hashable_state())

        successors = simpleRushHour.successors()

        for digestObject in successors:
            flag = 0
            for element in visited:
                digestObject.hashable_state().sort()
                #print(element)
                #print(digestObject.hashable_state())
                #print("----------")
                if(element == digestObject.hashable_state()):
                    flag = 1
            if not flag:
                toDigestObject.append(digestObject)
                toDigestCost.append(digestObject.gval)                
        print(len(visited))
    """
    return 2

def rushhour_goal_fn(state):
    #IMPLEMENT
    '''Have we reached a goal state'''
    vehicles = state.vehicles
    goalState = state.goalEntrance
    direction = state.goalDirection
    goalVehicle = getGoalVehicle(vehicles)
    boardX = state.numColumns
    boardY = state.numRows
    if(state.cells[goalState[1]][goalState[0]] != goalVehicle[0]):
        return False
    #if it's horizontal
    if(goalVehicle[3]):
        if(state.goalDirection == 'W'):
            newX = goalState[0] - 1
            if(newX < 0):
                newX = boardX - 1
            if(state.cells[goalState[1]][newX] == goalVehicle[0]):
                return False
        if(state.goalDirection == 'E'):
            newX = goalState[0] + 1
            if(newX >= boardX):
                newX = 0
            if(state.cells[goalState[1]][newX] == goalVehicle[0]):
                return False
        if(state.goalDirection == 'S' or state.goalDirection == 'N'):
            return False 
    else:
        if (state.goalDirection == 'N'):
            newY = goalState[1] - 1
            if(newY < 0):
                newY = boardY - 1
            if(state.cells[newY][goalState[0]] == goalVehicle[0]):
                return False
        if(state.goalDirection == 'S'):
            newY = goalState[1] + 1
            if(newY >= boardY):
                newY = 0
            if(state.cells[newY][goalState[0]] == goalVehicle[0]):
                return False
        if(state.goalDirection == 'E' or state.goalDirection == 'N'):
            return False 
    return True

def getGoalVehicle(vehicles):
    '''
    Find which vehicle is the goal vehicle and return that vehicle
    '''
    for vehicle in vehicles:
        if (vehicle[4] == True):
            return vehicle


def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction):
    #IMPLEMENT
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
      goal_entrance is the coordinates of the entrance tile to the goal and
      goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')

   NOTE: for simplicity you may assume that
         (a) no vehicle name is repeated
         (b) all locations are integer pairs (x,y) where 0<=x<=n-1 and 0<=y<=m-1
         (c) vehicle lengths are positive integers
    '''
    return rushhour("START",0, board_size[0], board_size[1], vehicle_list, goal_entrance, goal_direction)

    

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output.
    #Note that if you implement the "get" routines
    #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
    #properly, this function should work irrespective of how you represent
    #your state.
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board


def make_rand_init_state(nvehicles, board_size):
    '''Generate a random initial state containing
       nvehicles = number of vehicles
       board_size = (m,n) size of board
       Warning: may take a long time if the vehicles nearly
       fill the entire board. May run forever if finding
       a configuration is infeasible. Also will not work any
       vehicle name starts with a period.

       You may want to expand this function to create test cases.
    '''

    (m, n) = board_size
    vehicle_list = []
    board_properties = [board_size, None, None]
    for i in range(nvehicles):
        if i == 0:
            # make the goal vehicle and goal
            x = randint(0, n - 1)
            y = randint(0, m - 1)
            is_horizontal = True if randint(0, 1) else False
            vehicle_list.append(['gv', (x, y), 2, is_horizontal, True])
            if is_horizontal:
                board_properties[1] = ((x + n // 2 + 1) % n, y)
                board_properties[2] = 'W' if randint(0, 1) else 'E'
            else:
                board_properties[1] = (x, (y + m // 2 + 1) % m)
                board_properties[2] = 'N' if randint(0, 1) else 'S'
        else:
            board = get_board(vehicle_list, board_properties)
            conflict = True
            while conflict:
                x = randint(0, n - 1)
                y = randint(0, m - 1)
                is_horizontal = True if randint(0, 1) else False
                length = randint(2, 3)
                conflict = False
                for j in range(length):  # vehicle length
                    if is_horizontal:
                        if board[y][(x + j) % n] != '.':
                            conflict = True
                            break
                    else:
                        if board[(y + j) % m][x] != '.':
                            conflict = True
                            break
            vehicle_list.append([str(i), (x, y), length, is_horizontal, False])

    return make_init_state(board_size, vehicle_list, board_properties[1], board_properties[2])


def test(nvehicles, board_size):
    s0 = make_rand_init_state(nvehicles, board_size)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, rushhour_goal_fn, heur_min_moves)



if __name__ == '__main__':
    s = make_init_state((7, 7), [['gv', (1, 1), 2, True, True]], (4, 1), 'E')

        
    s.move_vehicle(['gv', (6, 6), 2, True, True], 'E')
    s.successors()   
