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

        self.plan_library = {
            "route_left": [[4,21],[4,3],[21,3],[21,2]],
            "route_middle": [[12,21],[12,13],[12,3],[21,3],[21,2]],
            "route_right": [[21,12], [21,2]],
        }

        self.current_plan = self.plan_library["route_left"]
        self.checkpoints_done = 0
        self.grid_size = None
        self.grid = None

        # initialize the first route to the first checkpoint
        self.route_to_checkpoint = None
        self.route_progress = 0


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

        goal = self.current_plan[self.checkpoints_done]
        loc = state[self.agent_properties["obj_id"]]['location']

        # check if destination reached
        if loc == tuple(self.current_plan[-1]):
            print("Destination reached!")
            return None, {}

        print(f"\nCurrently at {loc} with goal {goal} with checkpoint goal {self.current_plan[self.checkpoints_done]}")

        # upon initialization, calculate a route to the first checkpoint
        if self.route_to_checkpoint is None:
            self.route_to_checkpoint = astar(self.grid, loc, tuple(goal))
            print(f"Calculated new route to next checkpoint towards {goal}, route: {self.route_to_checkpoint}")

        # check if checkpoint reached or no path yet calculated
        if loc == tuple(self.current_plan[self.checkpoints_done]):
            print(f'Completed checkpoint {self.current_plan[self.checkpoints_done]}!')

            # check if destination reached
            if loc == tuple(self.current_plan[-1]):
                print("Destination reached!")
                return None, {}

            # get a route to the next checkpoint
            self.checkpoints_done += 1
            goal = self.current_plan[self.checkpoints_done]
            self.route_to_checkpoint = astar(self.grid, loc, tuple(goal))
            self.route_progress = 0
            print(f"Calculated new route to next checkpoint towards {goal}, route: {self.route_to_checkpoint}")


        # get our next step
        new_loc = self.route_to_checkpoint[self.route_progress]
        self.route_progress += 1
        action = self.move_to(loc, new_loc)
        print(f"Taking action {action} to get from {loc} to {new_loc} towards checkpoint {goal}")

        # # Select a random action
        # if possible_actions:
        #     action = self.rnd_gen.choice(possible_actions)
        # else:
        #     action = None

        action_kwargs = {}
        return action, action_kwargs


    def move_to(self, start, goal):
        """ Move in 1 position to the goal, by identifying which action to take and returning it """

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
