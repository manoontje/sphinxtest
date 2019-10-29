import random

from matrxs.actions.move_actions import MoveNorth, MoveEast, MoveSouth, MoveWest
from matrxs.agents.agent_brain import AgentBrain, AreaTile
from matrxs.agents.bw4t_brain import BW4TAgentBrain
from matrxs.agents.human_agent_brain import HumanAgentBrain
from matrxs.agents.patrolling_agent import PatrollingAgentBrain
from matrxs.objects.simple_objects import SquareBlock, Door
from matrxs.world_builder import WorldBuilder


def create_factory():
    factory = WorldBuilder(shape=[20, 20])

    autonomous_agent_1 = BW4TAgentBrain()
    autonomous_agent_2 = BW4TAgentBrain()

    factory.add_agent([11,9], autonomous_agent_1, name="Bot1",
                      visualize_shape='img', has_menu=True, img_name="explorervehicle.png")

    factory.add_agent([11, 11], autonomous_agent_2, name="Bot2",
                      visualize_shape='img', has_menu=True, img_name="explorervehicle.png")

    #Initialize blue room
    factory.add_room([3, 3], 5, 5, name="blue_room", door_locations=[(7, 5)])
    factory.add_object((4, 6), "blue_block_1", is_traversable=False, visualize_colour="#2e86c1")
    factory.add_object((5, 5), "blue_block_2", is_traversable=False, visualize_colour="#2e86c1")

    #Initialize red room
    factory.add_room([12, 3], 5, 5, name="red_room", door_locations=[(12, 5)])
    factory.add_object((13, 4), "red_block_1", is_traversable=False, visualize_colour="#e30202")
    factory.add_object((15, 6), "red_block_2", is_traversable=False, visualize_colour="#e30202")

    #Initialize yellow room
    factory.add_room([3, 12], 5, 5, name="yellow_room", door_locations=[(7, 14)])
    factory.add_object((5, 14), "yellow_block", is_traversable=False, visualize_colour="#fac800")
    factory.add_object((4, 13), "yellow_block", is_traversable=False, visualize_colour="#fac800")

    #Initialize green room
    factory.add_room([12, 12], 5, 5, name="green_room", door_locations=[(12, 14)])
    factory.add_object((15, 13), "green_block", is_traversable=False, visualize_colour="#60bf2c")
    factory.add_object((15, 14), "green_block", is_traversable=False, visualize_colour="#60bf2c")
    #Drop-off area
    factory.add_object((16,0), "dropoff", visualize_colour="#808080", callable_class=AreaTile)
    factory.add_object((17,0), "dropoff", visualize_colour="#808080", callable_class=AreaTile)
    factory.add_object((18,0), "dropoff", visualize_colour="#808080", callable_class=AreaTile)
    factory.add_object((19,0), "dropoff", visualize_colour="#808080", callable_class=AreaTile)

    return factory
