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

        self.block_orders = ['blue', 'green', 'green', 'red']




    def filter_observations(self, state):
        """
        Filtering the agent's observations.
        :param state:
        :return:
        """
        new_state = state.copy()
        closed_room_colors = []

        for k, obj in state.items():
            if 'door@' in k and obj.get('is_open') is False:
                color = k.split('_', 1)[0]
                closed_room_colors.append(color)
        for k, obj in state.items():
            for color in closed_room_colors:
                if (color in k) and ('doormat' not in k) and ('block' in k):
                    new_state.pop(k)

        self.state_tracker.update(new_state)
        return new_state

    def decide_on_action(self, state):
        """
        Decision of which action to perform.
        :param state:
        :return:
        """
        global cycle
        self.current_goal = self.goal_cycle[0]

        if len(self.block_orders) > 0:
            current_order = self.block_orders[0]
        else:
            return StandStill.__name__, {}

        this_agent = self.agent_id
        for k, obj in state.items():
            if 'Bot' in k and this_agent not in k:
                other_agent = k

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

        self.check_for_update(current_order)

        # Navigating to a room
        if self.current_goal == "find_room":
            # Setting location that is in front of a door
            self.navigator.reset_full()
            for doormat in doormats:
                doormat_id = doormats[doormat]['doormat_id']
                if current_order in doormat_id:
                    doormat_waypoint = doormats[doormat]['location']
                    self.navigator.add_waypoint(doormat_waypoint)
                    move_action = self.navigator.get_move_action(self.state_tracker)

            # Hacky way of going to the door that has not been opened yet.
                    current_waypoint = doormat_waypoint
                    if self.agent_properties['location'] == current_waypoint:
                        self.send_message(message_content={"id": doormat_id},
                                          to_id=other_agent)
                        self.goal_cycle.pop(0)

            return move_action, {}

        if self.current_goal == "open_door":
            for door in door_ids:
                if current_order in door:
                    door_id = door
            if state[door_id]['is_open'] == True:
                self.goal_cycle.pop(0)
            return OpenDoorAction.__name__, {'door_range': 1, 'object_id': door_id}

        if self.current_goal == "search_room":
            for block in blocks:
                if current_order in blocks[block]['block_id'] and blocks[block]['location'] not in return_area_locations:
                    block_location = blocks[block]['location']
            if self.agent_properties['location'] == block_location:
                self.goal_cycle.pop(0)
                return StandStill.__name__, {}
            else:
                self.navigator.reset_full()
                self.waypoints = block_location
                self.navigator.add_waypoint(self.waypoints)
                move_action = self.navigator.get_move_action(self.state_tracker)
                return move_action, {}

        if self.current_goal == "grab_block":

            for block in blocks:
                if current_order in blocks[block]['block_id'] and blocks[block]['location'] not in return_area_locations:
                    block_id = blocks[block]['block_id']
            self.goal_cycle.pop(0)
            return GrabObject.__name__, {'grab_range': 1, 'object_id' : block_id, 'max_objects': 1}

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
            self.goal_cycle.pop(0)
            self.goal_cycle = ["find_room", "open_door", "search_room", "grab_block", "to_dropoff", "drop_block",
                                   "done"]
            cycle += 1
            if cycle == len(door_ids):
                cycle = 0

            if len(self.block_orders) > 0:
                self.block_orders.pop(0)
            else:
                pass
            return DropObject.__name__, {}



        return StandStill.__name__, {}


    def check_for_update(self, current_order):
        for message in self.received_messages:
            print(message.content['id'])
            print(current_order)
            if current_order in message.content['id']:
                print('hierzooo')
                self.block_orders.pop(0)
                if len(self.block_orders) > 0:
                    current_order = self.block_orders[0]
                else:
                    StandStill.__name__, {}


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







