import random

from matrxs.agents.agent_brain import AgentBrain, OpenDoorAction, CloseDoorAction
from matrxs.utils.agent_utils.navigator import Navigator, MoveEast, MoveNorth, MoveSouth, MoveWest
from matrxs.utils.agent_utils.state_tracker import StateTracker

door_range = 10

class BW4TAgentBrain(AgentBrain):
    """This is the BW4TAgentBrain class.
    """

    def __init__(self, waypoints):
        super().__init__()
        self.state_tracker = None
        self.navigator = None
        self.waypoints = waypoints

    def initialize(self):
        """
        Initialization of the agent's state tracker.
        :return:
        """
        # Initialize this agent's state tracker
        self.state_tracker = StateTracker(agent_id=self.agent_id)

        self.navigator = Navigator(agent_id=self.agent_id, action_set=self.action_set,
                                   algorithm=Navigator.A_STAR_ALGORITHM)

        self.navigator.add_waypoints(self.waypoints, is_circular=True)

    def filter_observations(self, state):
        """
        Filtering the agent's observations.
        :param state:
        :return:
        """
        new_state = state.copy()
        for k, obj in state.items():
            new_state.pop(k)

        self.state_tracker.update(state)
        return state

    def decide_on_action(self, state):
        """
        Decision of which action to perform.
        :param state:
        :return:
        """


        moves = [MoveNorth.__name__,  MoveEast.__name__, MoveSouth.__name__, MoveWest.__name__]
        move_action = random.choices(moves, weights=[2,1,2,1], k=1)
        print(move_action)

        keys = state.keys()
        rooms = {}


        for k in keys:
            if 'room' in k:
                room_name = k.split(" - ")[0]
                if room_name not in rooms:
                    rooms[room_name] = None
                elif 'door' in k:
                    rooms[room_name] = {"door_id": k, "is_open": state[k]['is_open']}



        if self.agent_properties['location'] == (11,5):
            room = rooms['red_room']
            door = room['door_id']
            if room['is_open'] == True:
                return CloseDoorAction.__name__, {'door_range': 1, 'object_id': door}
            else:
                return OpenDoorAction.__name__, {'door_range': 1, 'object_id': door}

        elif self.agent_properties['location'] == (8,5):
            room = rooms['blue_room']
            door = room['door_id']
            if room['is_open'] == True:
                return CloseDoorAction.__name__, {'door_range': 1, 'object_id': door}
            else:
                return OpenDoorAction.__name__, {'door_range': 1, 'object_id': door}

        elif self.agent_properties['location'] == (8,14):
            room = rooms['yellow_room']
            door = room['door_id']
            if room['is_open'] == True:
                return CloseDoorAction.__name__, {'door_range': 1, 'object_id': door}
            else:
                return OpenDoorAction.__name__, {'door_range': 1, 'object_id': door}

        elif self.agent_properties['location'] == (11,14):
            room = rooms['green_room']
            door = room['door_id']
            if room['is_open'] == True:
                return CloseDoorAction.__name__, {'door_range': 1, 'object_id': door}
            else:
                return OpenDoorAction.__name__, {'door_range': 1, 'object_id': door}

        return move_action[0], {}





