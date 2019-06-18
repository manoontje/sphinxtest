from agents.agent import Agent
from agents.human_agent import HumanAgent
from scenario_manager.world_factory import RandomProperty, WorldFactory
from environment.actions.move_actions import *
from environment.actions.object_actions import *
from environment.objects.simple_objects import *
import sys
from itertools import chain, combinations



# Desert scenario
def create_factory():
    factory = WorldFactory(random_seed=1, shape=[25, 25], tick_duration=0.2, vis_bg="#c2b280")

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
                visualize_colour="#e9b92b", usrinp_action_map=usrinp_action_map)


    #############################################
    # Objects
    #############################################

    locations = [[0,0], [0,1], [10,11], [11,11], [12,11], [12,12]]
    factory.add_multiple_objects(locations=locations, names=["sand dune" for _ in range(len(locations))], \
                callable_classes=[Wall for _ in range(len(locations))], visualize_colours=["#e1bf92" for _ in range(len(locations))] )

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
