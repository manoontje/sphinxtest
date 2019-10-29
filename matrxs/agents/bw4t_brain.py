import random

from matrxs.agents.agent_brain import AgentBrain, OpenDoorAction, CloseDoorAction
from matrxs.utils.agent_utils.navigator import Navigator, MoveEast, MoveNorth, MoveSouth, MoveWest
from matrxs.utils.agent_utils.state_tracker import StateTracker

import re

door_range = 10

class BW4TAgentBrain(AgentBrain):
    """This is the BW4TAgentBrain class.
    """

    def __init__(self):
        super().__init__()
        self.state_tracker = None
        self.navigator = None
        self.goal_cycle = ["find_room", "open_door", "search_room", "grab_block", "return_block"]

    def initialize(self):
        """
        Initialization of the agent's state tracker.
        :return:
        """
        # Initialize this agent's state tracker
        self.state_tracker = StateTracker(agent_id=self.agent_id)

        self.navigator = Navigator(agent_id=self.agent_id, action_set=self.action_set,
                                   algorithm=Navigator.A_STAR_ALGORITHM)



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

        self.current_goal = self.goal_cycle[0]
        print(self.current_goal)

        objects = list(state.keys())
        doors = [obj for obj in objects
                 if 'class_inheritance' in state[obj] and state[obj]['class_inheritance'][0] == "Door"]
        door_locations = []
        door_ids = []
        for door in doors:
            door_ids.append(door)
            door_location = state[door]['location']
            door_locations.append(door_location)

        if self.current_goal == "find_room":
            self.waypoints = door_locations
            self.navigator.add_waypoints(self.waypoints, is_circular=True)
            move_action = self.navigator.get_move_action(self.state_tracker)
            return move_action, {}

        if self.current_goal == "open_door":
            pass
        if self.current_goal == "search_room":
            pass
        if self.current_goal == "grab_block":
            pass
        if self.current_goal == "return_block":
            pass

        return MoveSouth.__name__, {}



        # self.send_message(message_content={"room": {"name":"green_room", "room_contents": []}, "pickup": "square_block_124"}, to_id=None)
        #
        # self.received_messages
        #
        # self.current_goal = "search_room"
        #
        # if self.current_goal == "sr":
        #     pass
        # elif self.current_goal == "drop":
        #     pass







