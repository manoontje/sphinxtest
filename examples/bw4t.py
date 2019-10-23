import random

from matrxs.actions.move_actions import MoveNorth, MoveEast, MoveSouth, MoveWest
from matrxs.agents.agent_brain import AgentBrain
from matrxs.agents.bw4t_brain import BW4TAgentBrain
from matrxs.agents.human_agent_brain import HumanAgentBrain
from matrxs.agents.patrolling_agent import PatrollingAgentBrain
from matrxs.objects.simple_objects import SquareBlock
from matrxs.world_builder import WorldBuilder


def create_factory():
    factory = WorldBuilder(shape=[20, 20])

    autonomous_agent_1 = BW4TAgentBrain(waypoints=[(random.randrange(0, 20), random.randrange(0, 20)), (random.randrange(0, 20), random.randrange(0, 20))])
    autonomous_agent_2 = BW4TAgentBrain(waypoints=[(random.randrange(0, 20), random.randrange(0, 20)), (random.randrange(0, 20), random.randrange(0, 20))])

    factory.add_agent([9, 10], autonomous_agent_1, name="Bot1",
                      visualize_shape='img', has_menu=True, img_name="explorervehicle.png")

    factory.add_agent([11, 11], autonomous_agent_2, name="Bot2",
                      visualize_shape='img', has_menu=True, img_name="explorervehicle.png")

    #Initialize blue room
    factory.add_room([3, 3], 5, 5, name="blue_room", door_locations=[(7, 5)])
    factory.add_object((4, 6), SquareBlock((4, 6)).toJSON(), is_traversable=True, visualize_colour="#2e86c1")
    factory.add_object((5, 5), SquareBlock((5, 5)).toJSON(), is_traversable=True, visualize_colour="#2e86c1")

    #Initialize red room
    factory.add_room([12, 3], 5, 5, name="red_room", door_locations=[(12, 5)])
    factory.add_object((13, 4), SquareBlock((13, 4)).toJSON(), is_traversable=True, visualize_colour="#e30202")
    factory.add_object((15, 6), SquareBlock((15, 6)).toJSON(), is_traversable=True, visualize_colour="#e30202")

    #Initialize yellow room
    factory.add_room([3, 12], 5, 5, name="yellow_room", door_locations=[(7, 14)])
    factory.add_object((5, 14), SquareBlock((5, 14)).toJSON(), is_traversable=True, visualize_colour="#fac800")
    factory.add_object((4, 13), SquareBlock((4, 13)).toJSON(), is_traversable=True, visualize_colour="#fac800")

    #Initialize green room
    factory.add_room([12, 12], 5, 5, name="green_room", door_locations=[(12, 14)])
    factory.add_object((15, 13), SquareBlock((15, 13)).toJSON(), is_traversable=True, visualize_colour="#60bf2c")
    factory.add_object((15, 14), SquareBlock((15, 14)).toJSON(), is_traversable=True, visualize_colour="#60bf2c")

    return factory
