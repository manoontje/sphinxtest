import numpy as np
import heapq
from agents.agent_brain import AgentBrain

from environment.actions.object_actions import RemoveObject
from environment.actions.object_actions import GrabAction
from environment.actions.door_actions import *


class CL_agent(AgentBrain):

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
                    "speed": 1}
        }


        constraints = {   "time_limit": "not_set",
            "flying_speed": "not_set",
            "notify_more_often": False,
            "people_min_distance": "not_set",
            "prohibit_flying_over_water": "not_set",
            "dist_to_anti-air": "not_set",
            "dist_to_radar": "not_set"
        }

        # the plan the agent is executing
        self.current_plan, self.speed = self.interpret_constraints(constraints)

        print(f"plan: {self.current_plan}, speed:{self.speed}")


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
        # self.speed = self.plan_library[self.current_plan]["speed"]
        self.track_speed = 0


    def interpret_constraints(self, constraints):
        """
        An ultra simple agent planning algorithm based on constraintsselfself.
        Assumes the agent is based on the bottom right, and the goal on the top right.
        Agent can take three paths  towards the goal, via the left, middle or right.

        Below is the assumed version of the constraints on which the passed
        constraints should be based:
        constraints_simple = {
            # task specific constra ints
            "time_limit": ["not_set", "short", "long"], # short= 1-60 -> only short route, long=61-120 -> only short or medium route

            # drone configuration constraints
            "flying_speed": ["not_set", "low", "high"], # speed setting, low=1-5, high=6-10, default=5
            "notify_more_often": [False, True], # False = not_set, True = more often than default, default=once every x ticks
            # "notify_threshold": ["not_set", "low", "high"], # level = low=1-5, high=6-10, default=5

            # route constraints
            "people_min_distance": ["not_set", "medium", "high"], # % total size, also for houses, low=1-5, high=6-10, default=no/0
            "prohibit_flying_over_water": [False, True], # (default) False=not prohibited, True=prohibit, default=False
            "dist_to_anti-air": ["not_set", "low", "high"], # % (binned numerical value) low=1-5=50%chance crash, high=6-10=0%crash, default=high
            "dist_to_radar": ["not_set", "low", "high"] # (binned numerical value) low=1-5=50%chance detect, high=6-10=0%detect, default=high
        }

        To check:
        - default slow or high flying speed?
        - notify?
        - defaults of other constraints
        """

        # the three possible paths the agent can take, respectively left, middle and right
        plans = [0,1,2]
        loc_AA = 0 # location of the anti-air gun, indicating the option along which it stands
        loc_radar = 0 # location of the anti-air gun, indicating the option along which it stands
        loc_lake = 1 # location of the lake, indicating the option along which it stands
        loc_village = 2 # location of the village, indicating the option along which it stands

        # set speed constraint
        speed = 3 if constraints["flying_speed"] == "high" else 1

        # long time limit, we won't make the long route
        if constraints["time_limit"] == "long":
            plans = self.__remove_option([0],plans)

            # if we also fly slow, we won't make the medium length route as well
            # if constraints["flying_speed"] == "slow":
            #     plans = self.__remove_option([0],plans)

        # only short or medium routes possible with short time limit
        elif constraints["time_limit"] == "short":
            plans = self.__remove_option([0,1],plans)

            # no route possible if we also fly slow
            # if constraints["flying_speed"] == "slow":
            #     plans = self.__remove_option([0,1,2],plans)


        if constraints["prohibit_flying_over_water"]:
            plans = self.__remove_option(loc_lake, plans)

        if constraints["dist_to_anti-air"] == "high":
            plans = self.__remove_option(loc_AA, plans)

        if constraints["dist_to_radar"] == "high":
            plans = self.__remove_option(loc_radar, plans)

        if constraints["people_min_distance"] == "high":
            plans = self.__remove_option(loc_village, plans)


        # check if there are any options left
        if len(plans) == 0:
            raise Exception("No possible path to the goal complying with the constraints")

        # take the shortest path to the goal which complies with the constraints
        else:
            return plans[-1], speed



    def __remove_option(self, option, plans):
        """ Remove a possible plan from the possible plans """
        if type(option) == list:
            for opt in option:
                if opt in option:
                    plans.remove(opt)
        else:
            if option in plans:
                plans.remove(option)
        return plans



    def filter_observations(self, state):

        # get the grid size from the hidden info block on startup
        if self.grid_size == None:
            for ID in state:
                if "infoBlock" in ID:
                    self.grid_size = state[ID]["grid_size"]

        # initialize a dummy grid, normally you would have traversability of
        # objects noted in this grid
        self.grid = np.zeros(shape=self.grid_size, dtype=int)

        return state


    def decide_on_action(self, state, possible_actions):
        """
        The agent can execute one of multiple plans from its plan_library in a scenario.
        A plan consists of one or more routes, and additional settings such as the speed.
        Every route consists of checkpoints. Between checkpoints, a route is calculated
        with the A* path planning algorithm.
        """

        target_area_checked = False

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

                # change the colour of the target_area to green after surveillance
                # has been completed
                target_area_checked = True if self.routes_to_do[0] == "surveillance" else False

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


        # change target area to green if we completed surveillance in that area this iteration
        if target_area_checked:
            return "DeclareAreaChecked", {}

        # get our next step
        new_loc = self.route_to_checkpoint[self.route_progress]
        self.route_progress += 1
        action = self.move_to(loc, new_loc)

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
