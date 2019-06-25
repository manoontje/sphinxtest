from agents.agent import Agent
from agents.human_agent import HumanAgent
from scenario_manager.world_factory import RandomProperty, WorldFactory
from environment.actions.move_actions import *
from environment.actions.object_actions import *
from environment.objects.simple_objects import *
from environment.objects.cl_sc_objects import *
import sys
from itertools import chain, combinations
from colour import Color as Colour

# Scenario 4
# Context. Area: desert, area secured: no, intel: hostiles spotted.

def create_factory():
    # Environment
    # Urban (default / none)
    # Desert #d3ba90
    factory = WorldFactory(random_seed=1, shape=[25, 25], tick_duration=0.2, visualization_bg_clr="#d3ba90")

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
    factory.add_human_agent(location=[21, 21], agent=hu_ag, visualize_colour="#16e535",
            usrinp_action_map=usrinp_action_map)


    #############################################
    # Objects
    #############################################

    # lake
    factory.add_lake(name="lakeMacLakeFace", top_left_location=[8,9], width=8, height=6, fancy_colours=True)

    # road
    factory.add_area(top_left_location=[4, 21], width=17, height=1, name="road", visualize_colour="#999999") # south road
    factory.add_area(top_left_location=[4, 3], width=1, height=18, name="road", visualize_colour="#999999") # west road
    factory.add_area(top_left_location=[5, 3], width=17, height=1, name="road", visualize_colour="#999999") # north road
    factory.add_area(top_left_location=[21, 3], width=1, height=6, name="road", visualize_colour="#999999") # north west road
    factory.add_area(top_left_location=[21, 16], width=1, height=6, name="road", visualize_colour="#999999") # south west road
    factory.add_area(top_left_location=[0, 12], width=4, height=1, name="road", visualize_colour="#999999") # east connection west road


    # national alert status
    # green: #00FF00
    # orange: #ffa500
    # red: #FF0000
    factory.add_multiple_objects(locations=[[0,23],[0,24],[1,23],[1,24]], names="NationalAlertStatus", \
                visualize_colours="#00FF00", is_traversable=True )


    # fog
    factory.add_smoke_area(name="fog", top_left_location=[0,0], width=25, height=25, visualize_depth=101, smoke_thickness_multiplier=0.8)
    factory.add_smoke_area(name="fog", top_left_location=[6,7], width=12, height=10, visualize_depth=101, smoke_thickness_multiplier=1)


    # goal
    # not secured = "#000000"
    # secured = "#00FF00"
    locs = [[20,1], [20,3], [21,2], [22,1], [22,3]]
    factory.add_multiple_objects(locations=locs, visualize_colours="#000000", is_traversable=True)

    # Village
    # urban #545454
    # desert 7a370a
    houseColour = "#7a370a"
    house_base_locations = [[18, 11], [19, 13], [21, 14], [21, 11], [23, 12], [23, 15], [19,15], [17,15]]
    factory.add_multiple_objects(locations=house_base_locations, names="house_base", \
                callable_classes=HouseBase, visualize_colours=houseColour )
    house_roof_locations = [[18, 10], [19, 12], [21, 13], [21, 10], [23, 11], [23, 14], [19,14], [17,14]]
    factory.add_multiple_objects(locations=house_roof_locations, names="house_roof", \
                callable_classes=HouseRoof, visualize_colours=houseColour )


    # urbanize by placing houses
    factory.add_buildings(top_left_location=[4,1], width=15, height=2, density=0.05, visualize_colour=houseColour, name="house") # north
    factory.add_buildings(top_left_location=[5,5], width=15, height=3, density=0.05, visualize_colour=houseColour, name="house") # north 2
    factory.add_buildings(top_left_location=[5,16], width=15, height=4, density=0.05, visualize_colour=houseColour, name="house") # bottom
    factory.add_buildings(top_left_location=[3,23], width=18, height=2, density=0.05, visualize_colour=houseColour, name="house") # bottom 2
    factory.add_buildings(top_left_location=[0,1], width=3, height=11, density=0.05, visualize_colour=houseColour, name="house") # north east
    factory.add_buildings(top_left_location=[0,14], width=4, height=7, density=0.05, visualize_colour=houseColour, name="house") # south east

    return factory


def change_group_locations(loc, xIncr, yIncr):
    """ Can be used to transpose a group of locations all with a specific x and/or y value """
    print ("Base:", [[loc[0] + xIncr, loc[1] + yIncr] for loc in loc])
    print ("Base with y-1 (e.g. for house roof):", [[loc[0] + xIncr, loc[1] + yIncr - 1] for loc in loc])
