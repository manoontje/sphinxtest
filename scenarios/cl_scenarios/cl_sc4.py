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
    factory.add_human_agent(location=[21, 21], agent=hu_ag, visualize_depth=5,
                visualize_colour="#16e535", usrinp_action_map=usrinp_action_map)


    #############################################
    # Objects
    #############################################

    # Village
    houseColour = "#7a370a"
    house_base_locations = [[19, 13], [21, 14], [21, 11], [23, 12]]
    factory.add_multiple_objects(locations=house_base_locations, names=["house_base" for _ in range(len(house_base_locations))], \
                callable_classes=[HouseBase for _ in range(len(house_base_locations))], visualize_colours=[houseColour for _ in range(len(house_base_locations))] )
    house_roof_locations = [[19, 12], [21, 13], [21, 10], [23, 11]]
    factory.add_multiple_objects(locations=house_roof_locations, names=["house_roof" for _ in range(len(house_roof_locations))], \
                callable_classes=[HouseRoof for _ in range(len(house_roof_locations))], visualize_colours=[houseColour for _ in range(len(house_roof_locations))] )


    # lake
    factory.add_line(start=[11, 10], end=[14, 10], name="lake", callable_class=Water)
    factory.add_line(start=[10, 11], end=[15, 11], name="lake", callable_class=Water)
    factory.add_line(start=[9, 12], end=[16, 12], name="lake", callable_class=Water)
    factory.add_line(start=[9, 13], end=[16, 13], name="lake", callable_class=Water)
    factory.add_line(start=[10, 14], end=[15, 14], name="lake", callable_class=Water)
    factory.add_line(start=[10, 15], end=[14, 15], name="lake", callable_class=Water)


    # road
    factory.add_area(top_left_location=[4, 21], width=17, height=1, name="road", visualize_colour="#999999") # south road
    factory.add_area(top_left_location=[4, 3], width=1, height=18, name="road", visualize_colour="#999999") # west road
    factory.add_area(top_left_location=[5, 3], width=17, height=1, name="road", visualize_colour="#999999") # north road
    factory.add_area(top_left_location=[21, 3], width=1, height=6, name="road", visualize_colour="#999999") # north west road
    factory.add_area(top_left_location=[21, 16], width=1, height=6, name="road", visualize_colour="#999999") # south west road
    factory.add_area(top_left_location=[0, 12], width=4, height=1, name="road", visualize_colour="#999999") # east connection west road




    return factory


def change_group_locations(loc, xIncr, yIncr):
    print ("Base:", [[loc[0] + xIncr, loc[1] + yIncr] for loc in loc])
    print ("Roofs:", [[loc[0] + xIncr, loc[1] + yIncr - 1] for loc in loc])
