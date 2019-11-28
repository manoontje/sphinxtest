import math
import random

from matrxs.agents.agent_brain import AgentBrain, OpenDoorAction, CloseDoorAction, GrabObject, DropObject
from matrxs.utils.agent_utils.navigator import Navigator, MoveEast, MoveNorth, MoveSouth, MoveWest, StandStill
from matrxs.utils.agent_utils.state_tracker import StateTracker

import re

door_range = 10
cycle = 0


class BW4TAgentBrain_random(AgentBrain):
    """This is the BW4TAgentBrain class.
    """

    def __init__(self):
        super().__init__()
        self.state_tracker = None
        self.navigator = None
        self.block_orders = ['blue', 'yellow', 'green', 'red']


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

        self.block_orders = ['blue', 'yellow', 'green', 'red']




    def filter_observations(self, state):
        """
        Filtering the agent's observations.
        :param state:
        :return:
        """
        new_state = state.copy()

        objects = list(state.keys())
        closed_rooms = []
        for obj in objects:
            if 'door@' in obj and state[obj]['is_open'] == False:
                name = obj.split(' -')[0]
                closed_rooms.append((name, state[obj]['custom_properties']['object_locations']))

        for obj in objects:
            if 'block' in obj:
                for room in closed_rooms:
                    if state[obj]['location'] in room[1]:
                        new_state.pop(obj)

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
        #self.determine_room_content(state)

        self.check_for_update(current_order)

        doors = self.find_doors(state)[0]
        doormat_locations = self.find_doors(state)[1]
        delivery_area = self.determine_delivery_locations(state)
        known_blocks = self.determine_known_content(state, delivery_area)

        # Navigating to a room
        if self.current_goal == "find_room":
            if not known_blocks:
                for door in doormat_locations:
                    doormat_waypoint = door
                    if not self.agent_properties['location'] == doormat_waypoint:
                        self.navigator.reset_full()
                        self.navigator.add_waypoint(doormat_waypoint)
                        move_action = self.navigator.get_move_action(self.state_tracker)
                    else:
                        self.goal_cycle.pop(0)
                        move_action = StandStill.__name__
                    return move_action, {}
            else:
                if not any(current_order in item['name'] for item in known_blocks):
                # if current_order not in known_blocks['name']:
                    for door in doormat_locations:
                        doormat_waypoint = door
                        if not self.agent_properties['location'] == doormat_waypoint:
                            self.navigator.reset_full()
                            self.navigator.add_waypoint(doormat_waypoint)
                            move_action = self.navigator.get_move_action(self.state_tracker)
                        else:
                            self.goal_cycle.pop(0)
                            move_action = StandStill.__name__
                        return move_action, {}
                else:
                    self.goal_cycle.pop(0)
                    self.goal_cycle.pop(0)
                    return StandStill.__name__, {}

        if self.current_goal == "open_door":
            for door in doors:
                if math.sqrt( ((door['location'][0]-self.agent_properties['location'][0])**2)+((door['location'] [1]-self.agent_properties['location'][1])**2) ) < 2:
                    if door['is_open'] == True:
                        self.goal_cycle.pop(0)
                    return OpenDoorAction.__name__, {'door_range': 1, 'object_id': door['obj_id']}

            return StandStill.__name__, {}

        if self.current_goal == "search_room":
            if not any(current_order in item['name'] for item in known_blocks):
                self.goal_cycle = ["find_room", "open_door", "search_room", "grab_block",
                                                     "to_dropoff", "drop_block", "done"]
                return StandStill.__name__, {}
            else:
                for block in known_blocks:
                    if current_order in block['name']:
            #         for location in self.determine_delivery_locations(state):
            #             if block['location'] not in location:
                        block_location = block['location']
                        if self.agent_properties['location'] == block_location:
                            self.goal_cycle.pop(0)
                            return StandStill.__name__, {}
                        else:
                            self.navigator.reset_full()
                            self.waypoints = block_location
                            self.navigator.add_waypoint(self.waypoints)
                            move_action = self.navigator.get_move_action(self.state_tracker)
                            return move_action, {}


                # else:
                #     self.goal_cycle = ["find_room", "open_door", "search_room", "grab_block", "to_dropoff", "drop_block",
                #      "done"]
            return StandStill.__name__, {}


        if self.current_goal == "grab_block":
            for block in known_blocks:
                if current_order in block['name']:
                    # for location in self.determine_delivery_locations(state):
                    #     if block['location'] not in location:
                    block_id = block['obj_id']
                    self.goal_cycle.pop(0)
                    self.send_message(message_content={"id": block_id},
                                      to_id=other_agent)
                    return GrabObject.__name__, {'grab_range': 1, 'object_id': block_id, 'max_objects': 1}



        if self.current_goal == "to_dropoff":
            if self.agent_properties['is_carrying']:
                self.navigator.reset_full()
                waypoints = []
                for location in delivery_area:
                    waypoints.append(location[1])
                self.waypoints = waypoints[cycle]
                self.navigator.add_waypoint(self.waypoints)
                move_action = self.navigator.get_move_action(self.state_tracker)
                current_waypoint = self.waypoints
                if self.agent_properties['location'] == current_waypoint:
                    self.goal_cycle.pop(0)
                    return StandStill.__name__, {}
                return move_action, {}
            else:
                self.goal_cycle.pop(0)
                self.goal_cycle = ["find_room", "open_door", "search_room", "grab_block", "to_dropoff", "drop_block",
                               "done"]
                return StandStill.__name__, {}

        if self.current_goal == "drop_block":
            self.goal_cycle.pop(0)
            self.goal_cycle = ["find_room", "open_door", "search_room", "grab_block", "to_dropoff", "drop_block",
                               "done"]
            cycle += 1
            if cycle == len(delivery_area):
                cycle = 0

            if len(self.block_orders) > 0:
                self.block_orders.pop(0)
            else:
                pass
            return DropObject.__name__, {}


        return StandStill.__name__, {}


    def check_for_update(self, current_order):
        for message in self.received_messages:
            if current_order in message.content['id']:
                self.block_orders.pop(0)
                if len(self.block_orders) > 0:
                    current_order = self.block_orders[0]
                else:
                    StandStill.__name__, {}

    def get_order_length(self):
        return len(self.block_orders)

    def find_doors(self, state):
        doors = []
        doormat_locations = []
        objects = list(state.keys())
        for obj in objects:
            if 'door' in obj and not 'doormat' in obj:
                doors.append(state[obj])
                if not state[obj]['is_open']:
                    doormat_locations.append(state[obj]['custom_properties']['in_front_of_door'])
        return doors, doormat_locations


    def determine_known_content(self, state, delivery_area):
        objects = list(state.keys())
        known_blocks = []
        for obj in objects:
            if 'block' in obj and not any(state[obj]['location'] == location[1] for location in delivery_area):
                known_blocks.append(state[obj])
        return known_blocks

    def determine_delivery_locations(self,state):
        objects = list(state.keys())
        delivery_area = []
        for obj in objects:
            if 'drop' in obj:
                delivery_area.append((state[obj]['obj_id'], state[obj]['location']))
        return delivery_area






