from agents.agent import Agent
from agents.cl_agent import CL_agent
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
    agent = CL_agent()
    factory.add_agent(location=[21, 21], agent=agent, possible_actions=[MoveNorth.__name__, MoveEast.__name__, MoveSouth.__name__, MoveWest.__name__])


    #############################################
    # Human Agent
    #############################################

    # usr input action map for human agent
    # usrinp_action_map = {
    #     'w': MoveNorth.__name__,
    #     'd': MoveEast.__name__,
    #     's': MoveSouth.__name__,
    #     'a': MoveWest.__name__,
    #     'g': GrabAction.__name__,
    #     'p': DropAction.__name__
    # }
    #
    # hu_ag = HumanAgent()
    # factory.add_human_agent(location=[21, 21], agent=hu_ag, visualize_colour="#16e535",
    #         usrinp_action_map=usrinp_action_map)


    #############################################
    # Objects
    #############################################

    # info block with general info for agent
    factory.add_env_object(location=[0,10], name="infoBlock", visualize_opacity=0, visualize_colour="#000000", is_traversable=True, grid_size=factory.world_settings["shape"])

    # lake
    factory.add_lake(name="lakeMacLakeFace", top_left_location=[8,9], width=8, height=6, fancy_colours=True)

    # road
    factory.add_area(top_left_location=[4, 21], width=17, height=1, name="road", visualize_colour="#999999") # south road
    factory.add_area(top_left_location=[4, 3], width=1, height=18, name="road", visualize_colour="#999999") # west road
    factory.add_area(top_left_location=[5, 3], width=17, height=1, name="road", visualize_colour="#999999") # north road
    factory.add_area(top_left_location=[21, 3], width=1, height=19, name="road", visualize_colour="#999999") # north east road
    # factory.add_area(top_left_location=[21, 16], width=1, height=6, name="road", visualize_colour="#999999") # south east road
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
    house_base_locations = [[17,10],[19,10],[20,10],[17,13],[19,13],[22,11],[23,9],[24,11],[22,14],[23,16],[24,14]]
    factory.add_multiple_objects(locations=house_base_locations, names="house_base", \
                callable_classes=HouseBase, visualize_colours=houseColour )
    house_roof_locations = [[17,9],[19,9],[20,9],[17,12],[19,12],[22,10],[23,8],[24,10],[22,13],[23,15],[24,13]]
    factory.add_multiple_objects(locations=house_roof_locations, names="house_roof", \
                callable_classes=HouseRoof, visualize_colours=houseColour )
    locs = [[17,11],[18,11],[19,11],[20,11],[17,14],[18,14],[19,14],[20,14],[22,12],[23,12],[23,11],[23,10],[23,13],[23,14]]
    factory.add_multiple_objects(locations=locs, names="road", visualize_colours="#999999", is_traversable=True)

    # factory.add_buildings(top_left_location=[17,10], width=7, height=6, density=0.5, visualize_colour=houseColour, name="house") # village east


    # urbanize by placing houses
    factory.add_buildings(top_left_location=[4,2], width=15, height=1, density=0.2, visualize_colour=houseColour, name="house") # north
    factory.add_buildings(top_left_location=[5,5], width=15, height=1, density=0.2, visualize_colour=houseColour, name="house") # north 2
    factory.add_buildings(top_left_location=[5,19], width=15, height=2, density=0.2, visualize_colour=houseColour, name="house") # bottom
    factory.add_buildings(top_left_location=[3,23], width=18, height=2, density=0.2, visualize_colour=houseColour, name="house") # bottom 2
    factory.add_buildings(top_left_location=[2,1], width=1, height=11, density=0.2, visualize_colour=houseColour, name="house") # north east
    factory.add_buildings(top_left_location=[3,14], width=1, height=7, density=0.2, visualize_colour=houseColour, name="house") # south east



    # Routes visualization
    # locs = [[21,12], [21,2]]
    # factory.add_multiple_objects(locations=locs, names="waypoint_route1", visualize_colours="#00FF00", is_traversable=True )
    # locs = [[12,21],[12,13],[12,3],[21,3],[21,2]]
    # factory.add_multiple_objects(locations=locs, names="waypoint_route2", visualize_colours="#ffa500", is_traversable=True )
    # locs = [[4,21],[4,3],[21,3],[21,2]]
    # factory.add_multiple_objects(locations=locs, names="waypoint_route3", visualize_colours="#FF0000", is_traversable=True )

    return factory


def change_group_locations(loc, xIncr, yIncr):
    """ Can be used to transpose a group of locations all with a specific x and/or y value """
    print ("Base:", [[loc[0] + xIncr, loc[1] + yIncr] for loc in loc])
    print ("Base with y-1 (e.g. for house roof):", [[loc[0] + xIncr, loc[1] + yIncr - 1] for loc in loc])
