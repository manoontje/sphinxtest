from agents.agent import Agent
from agents.human_agent import HumanAgent
from scenario_manager.world_factory import RandomProperty, WorldFactory
from environment.actions.move_actions import *
from environment.actions.object_actions import *
from environment.objects.simple_objects import *
from environment.objects.cl_sc_objects import *
import sys
from itertools import chain, combinations


# Scenario 4
# Context. Area: desert, area secured: no, intel: hostiles spotted.

def create_factory():
    factory = WorldFactory(random_seed=1, shape=[25, 25], tick_duration=0.2, vis_bg="#d3ba90")

    #############################################
    # Agent
    #############################################
    # agent = Agent()
    # factory.add_agent(location=[1, 0], agent=agent, visualize_depth=5)


    #############################################
    # Human Agent
    #############################################

    # usr input action map for human agent
    usrinp_action_map = {
        'w': MoveNorth.__name__,
        'd': MoveEast.__name__,
        's': MoveSouth.__name__,
        'a': MoveWest.__name__,
        'g': GrabAction.__name__,
        'p': DropAction.__name__
    }

    hu_ag = HumanAgent()
    factory.add_human_agent(location=[4, 0], agent=hu_ag, visualize_depth=5,
                visualize_colour="#5d6773", usrinp_action_map=usrinp_action_map)


    #############################################
    # Objects
    #############################################

    # Obstacles
    # locations = [[0,0], [0,1], [10,11], [11,11], [12,11], [12,12]]
    # factory.add_multiple_objects(locations=locations, names=["sand dune" for _ in range(len(locations))], \
    #             callable_classes=[Wall for _ in range(len(locations))], visualize_colours=["#7a370a" for _ in range(len(locations))] )


    # Village
    houseColour = "#7a370a"
    locations = [[10,12], [12,13], [12,10], [14,11] ]
    factory.add_multiple_objects(locations=locations, names=["house_base" for _ in range(len(locations))], \
                callable_classes=[HouseBase for _ in range(len(locations))], visualize_colours=[houseColour for _ in range(len(locations))] )
    locations = [[10,11], [12,12], [12,9],  [14,10]]
    factory.add_multiple_objects(locations=locations, names=["house_roof" for _ in range(len(locations))], \
                callable_classes=[HouseRoof for _ in range(len(locations))], visualize_colours=[houseColour for _ in range(len(locations))] )


    # lake
    locations = [[16,14], [23, 23]]
    factory.add_multiple_objects(locations=locations, callable_classes=[Water for _ in range(len(locations))] )



   #  add_env_object(self, location, name, callable_class=None, customizable_properties=None,
   #                     is_traversable=None, is_movable=None,
   #                     visualize_size=None, visualize_shape=None, visualize_colour=None, visualize_depth=None,
   #                     **custom_properties):
   #
   # add_multiple_objects(self, locations, names=None, callable_classes=None, custom_properties=None,
   #                          customizable_properties=None, is_traversable=None, visualize_sizes=None,
   #                          visualize_shapes=None, visualize_colours=None, visualize_depths=None,
                            # is_movable=None):

    # factory.add_multiple_objects(locations=[[4, 4], [5, 5], [6, 6]])




    return factory
