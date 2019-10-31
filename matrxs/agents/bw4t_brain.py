import random

from matrxs.agents.agent_brain import AgentBrain, OpenDoorAction, CloseDoorAction, GrabObject, DropObject
from matrxs.utils.agent_utils.navigator import Navigator, MoveEast, MoveNorth, MoveSouth, MoveWest, StandStill
from matrxs.utils.agent_utils.state_tracker import StateTracker

import re

door_range = 10
cycle = 0

class BW4TAgentBrain(AgentBrain):
    """This is the BW4TAgentBrain class.
    """

    def __init__(self):
        super().__init__()
        self.state_tracker = None
        self.navigator = None


    def initialize(self):
        """
        Initialization of the agent's state tracker.
        :return:
        """
        # Initialize this agent's state tracker
        self.state_tracker = StateTracker(agent_id=self.agent_id)

        self.navigator = Navigator(agent_id=self.agent_id, action_set=self.action_set,
                                   algorithm=Navigator.A_STAR_ALGORITHM)

        self.goal_cycle = ["find_room", "open_door", "search_room", "grab_block", "to_dropoff" ,"drop_block", "done"]



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
        global cycle
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

        doormats = {}
        doormat_locations = []
        for obj in objects:
            if 'doormat' in obj:
                doormats[obj] = {'doormat_id': obj, 'location': state[obj]['location']}
                doormat_locations.append(state[obj]['location'])

        blocks = {}
        block_locations = []
        block_ids = []
        for obj in objects:
            if 'block' in obj:
                blocks[obj] = {'block_id': obj, 'location': state[obj]['location']}
                block_locations.append(state[obj]['location'])
                block_ids.append(obj)

        return_area_ids = []
        return_area_locations = []
        for obj in objects:
            if 'drop' in obj:
                return_area_ids.append(obj)
                return_area_locations.append(state[obj]['location'])

        blocks_delivered = []
        for block in blocks:
            if blocks[block]['location'] in return_area_locations:
                blocks_delivered.append(block)
        print("Lengtes ", len(blocks_delivered), len(block_ids))

        # Navigating to a room
        if self.current_goal == "find_room":
            # Setting location that are in front of a door
            self.navigator.reset_full()
            doormat_waypoint = doormat_locations[cycle]
            self.navigator.add_waypoint(doormat_waypoint)
            move_action = self.navigator.get_move_action(self.state_tracker)

            # Hacky way of going to the door that has not been opened yet.
            current_waypoint = doormat_waypoint
            print(self.agent_properties['location'], current_waypoint)
            if self.agent_properties['location'] == current_waypoint:
                self.goal_cycle.pop(0)
                print(self.goal_cycle, doormat_waypoint)
                return StandStill.__name__, {}
            return move_action, {}

        if self.current_goal == "open_door":
            door_id = door_ids[cycle]
            print("location is ", self.agent_properties['location'])
            if state[door_id]['is_open'] == True:
                self.goal_cycle.pop(0)
            return OpenDoorAction.__name__, {'door_range': 1, 'object_id': door_id}

        if self.current_goal == "search_room":
            if self.agent_properties['location'] == block_locations[cycle]:
                self.goal_cycle.pop(0)
                return StandStill.__name__, {}
            else:
                self.navigator.reset_full()
                self.waypoints = block_locations[cycle]
                self.navigator.add_waypoint(self.waypoints)
                move_action = self.navigator.get_move_action(self.state_tracker)
                return move_action, {}

        if self.current_goal == "grab_block":
            self.goal_cycle.pop(0)
            block_id = block_ids[cycle]
            print(block_id)
            return GrabObject.__name__, {'grab_range': 1, 'object_id' : block_ids[cycle], 'max_objects': 1}

        if self.current_goal == "to_dropoff":
            self.navigator.reset_full()
            self.waypoints = return_area_locations[cycle]
            self.navigator.add_waypoint(self.waypoints)
            move_action = self.navigator.get_move_action(self.state_tracker)
            current_waypoint = self.waypoints
            if self.agent_properties['location'] == current_waypoint:
                self.goal_cycle.pop(0)
                return StandStill.__name__, {}
            return move_action, {}

        if self.current_goal == "drop_block":
            if len(blocks_delivered) == len(block_ids):

                return StandStill.__name__, {}
            else:
                self.goal_cycle.pop(0)
                self.goal_cycle = ["find_room", "open_door", "search_room", "grab_block", "to_dropoff", "drop_block", "done"]
                cycle += 1
                if cycle == len(door_ids):
                    cycle = 0
            return DropObject.__name__, {}







        return StandStill.__name__, {}



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







