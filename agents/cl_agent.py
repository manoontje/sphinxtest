import numpy as np
import heapq
from agents.agent import Agent

from environment.actions.object_actions import RemoveObject
from environment.actions.object_actions import GrabAction
from environment.actions.door_actions import *


class CL_agent(Agent):

    def __init__(self):
        super().__init__()
        print("Hello, I am cl_agent")


        self.possible_routes = {
            "route_left": [[4,21],[4,3],[21,3],[21,2]],
            "route_left_reverse": [[21,2],[21, 3], [4, 3], [4, 21], [21, 21]],
            "route_middle": [[12,21],[12,13],[12,3],[21,3],[21,2]],
            "route_middle_reverse": [[21,2],[21, 3],[12,3], [12, 13], [12, 21], [21, 21]],
            "route_right": [[21,12], [21,2]],
            "route_right_reverse": [[21,2],[21,12], [21, 21]],
            "surveillance": [[22,3], [22,1], [20,1], [20,3], [22,3], [22,1], [20,1], [20,3], [22,3], [22,1], [20,1], [20,3]],
        }

        self.plan_library = {
            0: {    "routes": ["route_left", "surveillance", "route_left_reverse"],
                    "speed": 1},
            1: {    "routes": ["route_middle", "surveillance", "route_middle_reverse"],
                    "speed": 1},
            2: {    "routes": ["route_right", "surveillance", "route_right_reverse"],
                    "speed": 1},
            3: {    "routes": ["route_left", "surveillance", "route_left_reverse"],
                    "speed": 3},
            4: {    "routes": ["route_middle", "surveillance", "route_middle_reverse"],
                    "speed": 3},
            5: {    "routes": ["route_right", "surveillance", "route_right_reverse"],
                    "speed": 3}
        }

        # the plan the agent is executing
        self.current_plan = 5

        # the routes which the agent has to complete
        self.routes_to_do = self.plan_library[self.current_plan]["routes"]
        self.current_route = None
        self.checkpoints_done = 0
        self.grid_size = None
        self.grid = None

        # initialize the first route to the first checkpoint
        self.route_to_checkpoint = None
        self.route_progress = 0

        # keep track of speed, higher is slower. 1 is max
        self.speed = self.plan_library[self.current_plan]["speed"]
        self.track_speed = 0



    def ooda_observe(self, state):

        # get the grid size from the hidden info block on startup
        if self.grid_size == None:
            for ID in state:
                if "infoBlock" in ID:
                    self.grid_size = state[ID]["grid_size"]

        # initialize a dummy grid, normally you would have traversability of
        # objects noted in this grid
        self.grid = np.zeros(shape=self.grid_size, dtype=int)

        return state


    def ooda_decide(self, state, possible_actions):
        """
        The agent can execute one of multiple plans from its plan_library in a scenario.
        A plan consists of one or more routes, and additional settings such as the speed.
        Every route consists of checkpoints. Between checkpoints, a route is calculated
        with the A* path planning algorithm.
        """

        can_move = self.done_moving()

        if not can_move:
            # print("Waiting for completion of the previous movement")
            return None, {}

        # initialize the first route on the first execution of the agent
        if self.current_route is None:
            self.set_new_route()

        goal = self.current_route[self.checkpoints_done]
        loc = state[self.agent_properties["obj_id"]]['location']

        # check if destination reached
        if len(self.routes_to_do) == 0:
            print("Plan completed!")
            return None, {}

        # upon first execution, calculate a path to the first checkpoint
        if self.route_to_checkpoint is None:
            self.route_to_checkpoint = astar(self.grid, loc, tuple(goal))
            print(f"Calculated new route to next checkpoint towards {goal}, route: {self.route_to_checkpoint}")

        # check if checkpoint reached or no path yet calculated
        if loc == tuple(self.current_route[self.checkpoints_done]):
            print(f'Completed checkpoint {self.current_route[self.checkpoints_done]}!')
            self.checkpoints_done += 1

            # check if route completed
            if self.checkpoints_done == len(self.current_route):
                print(f"Route '{self.routes_to_do[0]}' completed!")
                # done with this route so delete it
                del self.routes_to_do[0]

                # check if plan completed
                if len(self.routes_to_do) == 0:
                    print("Plan completed!")
                    self.checkpoints_done = 0
                    return None, {}

                self.set_new_route()


            # get a route to the next checkpoint
            goal = self.current_route[self.checkpoints_done]
            self.route_to_checkpoint = astar(self.grid, loc, tuple(goal))
            self.route_progress = 0
            print(f"Calculated new route to next checkpoint towards {goal}, route: {self.route_to_checkpoint}")


        # get our next step
        new_loc = self.route_to_checkpoint[self.route_progress]
        self.route_progress += 1
        action = self.move_to(loc, new_loc)

        # # Select a random action
        # if possible_actions:
        #     action = self.rnd_gen.choice(possible_actions)
        # else:
        #     action = None

        action_kwargs = {}
        return action, action_kwargs


    def done_moving(self):
        """
        If we have an agent with slower speed, it takes longer to execute a movement,
        that is, it may only execute that action every x (=speed setting value) ticks.
        Returns True if an action can be executed, returns False if not
        """
        self.track_speed += 1

        # we can execute an action!
        if self.track_speed == self.speed:
            self.track_speed = 0
            return True

        # agent still busy with previous movement, wait
        return False


    def set_new_route(self):
        """ Get the next route in the plan """
        self.current_route = self.possible_routes[self.routes_to_do[0]]
        self.checkpoints_done = 0
        self.route_progress = 0
        print(f"Starting new route {self.routes_to_do[0]}")



    def move_to(self, start, goal):
        """ Figure out which action we have to take to get to the next position """

        if goal[0] > start[0]:
            return "MoveEast"
        elif goal[0] < start[0]:
            return "MoveWest"
        elif goal[1] > start[1]:
            return "MoveSouth"
        elif goal[1] < start[1]:
            return "MoveNorth"



def heuristic(a, b):
    """ heuristic function for path scoring """
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def astar(array, start, goal):
    """
    A star algorithm, returns the shortest path to get from goal to start.
    Uses an 2D numpy array, with 0 being traversable, anything else (e.g. 1) not traversable
    Implementation from: https://www.analytics-link.com/single-post/2018/09/14/Applying-the-A-Path-Finding-Algorithm-in-Python-Part-1-2D-square-grid
    """

    # possible movements
    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] != 0:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
