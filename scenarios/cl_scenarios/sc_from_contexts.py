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


def create_factory(file, scenario_n, simulation_goal=0):
    # get scenario
    settings = fetch_settings(file, scenario_n)

    print("creating factory with settings:\n", settings)

    # Environment
    road_colour = "#838383" if settings['area_type'] == "mountainous" else "#999999"
    houseColour = "#2f2f2f" if settings['area_type'] == "mountainous" else "#545454"

    # BG colour: Urban #C2C2C2 - Desert #d3ba90 - mountaineous #556732
    bg_colour = "#556732" if settings['area_type'] == "mountainous" else "#C2C2C2"

    # create the world with a simulation goal or not, depending on user settings
    if simulation_goal > 0:
        factory = WorldFactory( random_seed=1, shape=[25, 25], tick_duration=0.2,
                visualization_bg_clr=bg_colour, simulation_goal=simulation_goal)
    else:
        factory = WorldFactory( random_seed=1, shape=[25, 25], tick_duration=0.2,
                visualization_bg_clr=bg_colour)

    #############################################
    # Agent
    #############################################
    agent = CL_agent()
    if not settings['nighttime']:
        factory.add_agent(location=[21, 21], agent=agent, name="drone", visualize_shape="img",
                    img_name="drone.png", visualize_depth=103,
                    possible_actions=[  MoveNorth.__name__, MoveEast.__name__,
                                        MoveSouth.__name__, MoveWest.__name__,
                                        DeclareAreaChecked.__name__])
    else:
        factory.add_agent(location=[21, 21], agent=agent, name="drone", visualize_shape="img",
                    img_name="drone_night.png", visualize_depth=110, visualize_size=2.0,
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

    ## Barracks
    factory.add_env_object(location=[23, 22], name="Barracks", visualize_size=3.0,
            visualize_shape="img", img_name="barracks.png", visualize_depth=106)
    # road to barracks
    factory.add_area(top_left_location=[21, 21], width=1, height=3, name="road",
                visualize_colour=road_colour) # bit down
    factory.add_area(top_left_location=[21, 24], width=3, height=1, name="road",
                visualize_colour=road_colour) # to the right


    ## lake [9,9]-[15,14]
    factory.add_line(start=[12,9], end=[13,9], name="laceMacLakeFace", callable_class=Water)
    factory.add_line(start=[9,10], end=[14,10], name="laceMacLakeFace", callable_class=Water)
    factory.add_line(start=[8,11], end=[14,11], name="laceMacLakeFace", callable_class=Water)
    factory.add_line(start=[8,12], end=[15,12], name="laceMacLakeFace", callable_class=Water)
    factory.add_line(start=[9,13], end=[15,13], name="laceMacLakeFace", callable_class=Water)
    factory.add_line(start=[10,14], end=[14,14], name="laceMacLakeFace", callable_class=Water)
    # factory.add_lake(name="lakeMacLakeFace", top_left_location=[8,9], width=8,
                # height=6, fancy_colours=True)


    ## rubber ducky
    # factory.add_env_object(location=[10,13], name="rubber_duck",
                # visualize_colour="#efff01", visualize_size=0.2, is_traversable=True)

    ## road
    factory.add_area(top_left_location=[4, 21], width=17, height=1, name="road",
                visualize_colour=road_colour) # south road
    factory.add_area(top_left_location=[4, 3], width=1, height=18, name="road",
                visualize_colour=road_colour) # west road
    factory.add_area(top_left_location=[5, 3], width=17, height=1, name="road",
                visualize_colour=road_colour) # north road
    factory.add_area(top_left_location=[21, 3], width=1, height=19, name="road",
                visualize_colour=road_colour) # north east road
    factory.add_area(top_left_location=[0, 12], width=4, height=1, name="road",
                visualize_colour=road_colour) # east connection west road


    ############## Estimated intel_hostiles_in_village ###################
    # orange: #ffa500 - red: #FF0000
    # houseColour = "#ffa500" if settings['intel_hostiles_in_village'] else "#545454"
    #

    ## Village
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
                 visualize_colours=road_colour, is_traversable=True)

    # factory.add_buildings(top_left_location=[17,10], width=7, height=6, density=0.5, visualize_colour=houseColour, name="house") # village east



    ############## Estimated Environment Threat Level ###################
    # code_green: #00FF00 - code_orange: #ffa500 - code_red: #FF0000
    # clr = "#00FF00"
    # if settings['estimated_threat_env'] == "code_orange":
    #     clr = "#ffa500"
    # elif settings['estimated_threat_env'] == "code_red":
    #     clr = "#FF0000"
    # locs = [[0,23],[0,24],[1,23],[1,24]]
    # factory.add_multiple_objects(locations=locs,
    #             names="NationalAlertStatus", visualize_colours=clr,
    #             is_traversable=True, visualize_depths=[105]*len(locs) )


    ############## Weather ###################
    ## fog
    fog_depth = 111 if settings['nighttime'] else 104
    smoke_thickness_multiplier = 0.6
    if settings['nighttime']:
        smoke_thickness_multiplier = 0.4
    elif settings['area_type'] == 'urban':
        smoke_thickness_multiplier = 1.2

    if settings['weather'] == "fog":
        factory.add_smoke_area(name="fog", top_left_location=[0,0],
                width=factory.world_settings["shape"][0],
                height=factory.world_settings["shape"][1], visualize_depth=fog_depth,
                smoke_thickness_multiplier=smoke_thickness_multiplier)
        # factory.add_smoke_area(name="fog", top_left_location=[6,7], width=12, height=10,
        #         visualize_depth=101, smoke_thickness_multiplier=1)

    ## heavy winds
    # God agent doing god things (i.e. stirring water to simulate wind)
    agent = God_agent()
    factory.add_agent(location=[21, 21], agent=agent, name="god", is_traversable=True,
                visualize_opacity=0.0, possible_actions=[StirWater.__name__])



    ############## Nighttime ###################
    # 0.0 = clear day, 1.0 = night (pitch black)
    intel_depth = 106
    if settings['nighttime']:
        factory.time_of_day(top_left_location=[0,0], width=factory.world_settings["shape"][0],
                height=factory.world_settings["shape"][1], name="dark_of_the_night",
                visualize_colour="#000000", nighttime=0.6, visualize_depth=105)
        intel_depth = 106





    ############## (Intel) VIP inbound at x ###################
    if settings['intel_vip_inbound']:
        print("Adding VIP inbound notification")
        factory.add_env_object(location=[1,12], name="VIP_inbound_notification",
                callable_class=VIP_inbound_notification, visualize_size=3.0,
                visualize_shape="img", img_name="incoming_vip.png", visualize_depth=intel_depth)


    ############## (Intel) AA gun at x ###################
    if settings['intel_anti-air_at_x']:
        if not settings['nighttime'] or settings['weather'] == "fog":
            factory.add_env_object(location=[2,5], name="AA_gun", callable_class=AA_gun,
                    visualize_shape="img", img_name="AA.png", visualize_size=2.0,
                    visualize_depth=intel_depth)
        else:
            factory.add_env_object(location=[2,5], name="AA_gun", callable_class=AA_gun,
                    visualize_shape="img", img_name="AA_night.png", visualize_size=2.0,
                    visualize_depth=intel_depth)

    ############## (Intel) Radar at x ###################
    if settings['intel_radar_at_x']:
        if not settings['nighttime'] or settings['weather'] == "fog":
            factory.add_env_object(location=[2,7], name="radar", callable_class=Radar,
                    visualize_shape="img", img_name="radar.png", visualize_size=2.0,
                    visualize_depth=intel_depth)
        else:
            factory.add_env_object(location=[2,7], name="radar", callable_class=Radar,
                    visualize_shape="img", img_name="radar_night.png", visualize_size=2.0,
                    visualize_depth=intel_depth)


    ############## (Intel) hostiles_in_village ###################
    if settings['intel_hostiles_in_village']:
        factory.add_env_object(location=[21,12], name="Yellow warning", is_traversable=True,
                visualize_shape="img", img_name="yellow_warning.png", visualize_size=2.0,
                visualize_depth=intel_depth)


    ############## Area Secured ###################
    # goal
    # not secured = "#000000" -  secured = "#00FF00"
    clr = "#000000" # if settings['area_secured'] else "#00FF00"
    locs = [[20,1], [20,3], [21,2], [22,1], [22,3]]
    factory.add_multiple_objects(locations=locs, visualize_colours=clr, visualize_depths=[intel_depth]*len(locs),
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
