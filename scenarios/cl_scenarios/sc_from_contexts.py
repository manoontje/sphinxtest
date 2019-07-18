import pandas as pd
from agents.agent_brain import AgentBrain
from agents.cl_agent import CL_agent
from agents.god_agent import God_agent
from agents.human_agent_brain import HumanAgentBrain
from world_factory.world_factory import RandomProperty, WorldFactory
from environment.actions.move_actions import *
from environment.actions.object_actions import *
from environment.actions.cl_actions import *
from environment.objects.simple_objects import *
from environment.objects.cl_sc_objects import *
import sys
from itertools import chain, combinations
from colour import Color as Colour

# Below is the assumed version of the contexts used for the creation of contexts.csv
# contexts = {
#     # natural environment context
#     "area_type": ["urban", "desert"],
#     "weather": ["clear", "fog", "heavy_winds"],
#     "nighttime": [False, True], # ["day", "night"]
#
#     # mission specific environment context vars
#     "area_secured": [False, True], # ["area_not_sec", "area_secured"]
#     "intel_radar_at_x": [False, True],
#     "intel_anti-air_at_x": [False, True], # ["anti_air_not_present_at_x", "anti_air_present_at_x"]
#     "intel_vip_inbound": [False, True], # numerical feature / range
#     "estimated_threat_env": ["code_green", "code_orange", "code_red"] # multi-class, attitude towards agent
# }


def create_factory(file, scenario_n):
    # get scenario
    settings = fetch_settings(file, scenario_n)

    print("creating factory with settings:\n", settings)

    # Environment
    # BG colour: Urban (grey, default this colour) - Desert #d3ba90
    bg_colour = "#d3ba90" if settings['area_type'] == "Desert" else "#C2C2C2"
    factory = WorldFactory( random_seed=1, shape=[25, 25], tick_duration=0.2,
                visualization_bg_clr=bg_colour)

    #############################################
    # Agent
    #############################################
    agent = CL_agent()
    factory.add_agent(location=[21, 21], agent=agent, name="drone", visualize_shape="img",
                img_name="drone.png", visualize_depth=103,
                possible_actions=[  MoveNorth.__name__, MoveEast.__name__,
                                    MoveSouth.__name__, MoveWest.__name__,
                                    DeclareAreaChecked.__name__])


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

    ############## General environment objects ###################

    ## info block with general info for agent
    factory.add_env_object(location=[0,10], name="infoBlock",
                visualize_opacity=0, visualize_colour="#000000", is_traversable=True,
                grid_size=factory.world_settings["shape"])

    ## lake
    factory.add_lake(name="lakeMacLakeFace", top_left_location=[8,9], width=8,
                height=6, fancy_colours=True)

    ## rubber ducky
    factory.add_env_object(location=[10,13], name="rubber_duck",
                visualize_colour="#efff01", visualize_size=0.2, is_traversable=True)

    ## road
    factory.add_area(top_left_location=[4, 21], width=17, height=1, name="road",
                visualize_colour="#999999") # south road
    factory.add_area(top_left_location=[4, 3], width=1, height=18, name="road",
                visualize_colour="#999999") # west road
    factory.add_area(top_left_location=[5, 3], width=17, height=1, name="road",
                visualize_colour="#999999") # north road
    factory.add_area(top_left_location=[21, 3], width=1, height=19, name="road",
                visualize_colour="#999999") # north east road
    factory.add_area(top_left_location=[0, 12], width=4, height=1, name="road",
                visualize_colour="#999999") # east connection west road

    ## Village
    # House colour: urban #545454 - desert 7a370a
    houseColour = "#d3ba90" if settings['area_type'] == "Desert" else "#545454"
    house_base_locations = [[17,10],[19,10],[20,10],[17,13],[19,13],[22,11],
                            [23,9],[24,11],[22,14],[23,16],[24,14]]
    factory.add_multiple_objects(locations=house_base_locations, names="house_base",
                callable_classes=HouseBase, visualize_colours=houseColour )

    house_roof_locations = [[17,9],[19,9],[20,9],[17,12],[19,12],[22,10],[23,8],
                            [24,10],[22,13],[23,15],[24,13]]
    factory.add_multiple_objects(locations=house_roof_locations, names="house_roof",
                callable_classes=HouseRoof, visualize_colours=houseColour )

    locs = [[17,11],[18,11],[19,11],[20,11],[17,14],[18,14],[19,14],[20,14],
            [22,12],[23,12],[23,11],[23,10],[23,13],[23,14]]
    factory.add_multiple_objects(locations=locs, names="road",
                 visualize_colours="#999999", is_traversable=True)

    # factory.add_buildings(top_left_location=[17,10], width=7, height=6, density=0.5, visualize_colour=houseColour, name="house") # village east


    ############## Estimated Environment Threat Level ###################
    # code_green: #00FF00 - code_orange: #ffa500 - code_red: #FF0000
    clr = "#00FF00"
    if settings['estimated_threat_env'] == "code_orange":
        clr = "#ffa500"
    elif settings['estimated_threat_env'] == "code_red":
        clr = "#FF0000"
    locs = [[0,23],[0,24],[1,23],[1,24]]
    factory.add_multiple_objects(locations=locs,
                names="NationalAlertStatus", visualize_colours=clr,
                is_traversable=True, visualize_depths=[105]*len(locs) )


    ############## Weather ###################
    ## fog
    if settings['weather'] == "fog":
        factory.add_smoke_area(name="fog", top_left_location=[0,0],
                width=factory.world_settings["shape"][0],
                height=factory.world_settings["shape"][1], visualize_depth=104,
                smoke_thickness_multiplier=0.8)
        factory.add_smoke_area(name="fog", top_left_location=[6,7], width=12, height=10,
                visualize_depth=101, smoke_thickness_multiplier=1)

    ## heavy winds
    # God agent doing god things (i.e. stirring water to simulate wind)
    agent = God_agent()
    factory.add_agent(location=[21, 21], agent=agent, name="god", is_traversable=True,
                visualize_opacity=0.0, possible_actions=[StirWater.__name__])



    ############## Nighttime ###################
    # 0.0 = clear day, 1.0 = night (pitch black)
    if settings['nighttime']:
        factory.time_of_day(top_left_location=[0,0], width=factory.world_settings["shape"][0],
                height=factory.world_settings["shape"][1], name="dark_of_the_night",
                visualize_colour="#000000", nighttime=0.4, visualize_depth=105)



    ############## (Intel) VIP inbound at x ###################
    if settings['intel_vip_inbound']:
        print("Adding VIP inbound notification")
        factory.add_env_object(location=[1,12], name="VIP_inbound_notification",
                callable_class=VIP_inbound_notification, visualize_size=3.0,
                visualize_shape="img", img_name="incoming_vip.png")


    ############## (Intel) AA gun at x ###################
    if settings['intel_anti-air_at_x']:
        factory.add_env_object(location=[2,5], name="AA_gun", callable_class=AA_gun,
                visualize_shape="img", img_name="AA.png", visualize_size=2.0,
                visualize_depth=101)


    ############## (Intel) Radar at x ###################
    if settings['intel_radar_at_x']:
        factory.add_env_object(location=[2,7], name="radar", callable_class=Radar,
                visualize_shape="img", img_name="radar.png", visualize_size=2.0,
                visualize_depth=101)


    ############## Area Secured ###################
    # goal
    # not secured = "#000000" -  secured = "#00FF00"
    clr = "#000000" if settings['area_secured'] else "#00FF00"
    locs = [[20,1], [20,3], [21,2], [22,1], [22,3]]
    factory.add_multiple_objects(locations=locs, visualize_colours=clr,
                is_traversable=True, names="target_area")


    ############## Area Type: Urban ###################
    if settings['area_type'] == "urban":
        # urbanize by placing houses
        factory.add_buildings(top_left_location=[4,2], width=15, height=1,
                density=0.2, visualize_colour=houseColour, name="house") # north
        factory.add_buildings(top_left_location=[5,5], width=15, height=1,
                density=0.2, visualize_colour=houseColour, name="house") # north 2
        factory.add_buildings(top_left_location=[5,19], width=15, height=2,
                density=0.2, visualize_colour=houseColour, name="house") # bottom
        factory.add_buildings(top_left_location=[3,23], width=18, height=2,
                density=0.2, visualize_colour=houseColour, name="house") # bottom 2
        factory.add_buildings(top_left_location=[2,1], width=1, height=11,
                density=0.2, visualize_colour=houseColour, name="house") # north east
        factory.add_buildings(top_left_location=[3,14], width=1, height=7,
                density=0.2, visualize_colour=houseColour, name="house") # south east



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





def fetch_settings(fl, scenario_n):
    # read in data of that specific scenario
    df = pd.read_csv(fl)
    settings = df.iloc[scenario_n,:]
    return settings



if __name__== "__main__":
    create_factory(1)
