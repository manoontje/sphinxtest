from matrxs.actions.move_actions import MoveNorth, MoveEast, MoveSouth, MoveWest
from matrxs.agents.human_agent_brain import HumanAgentBrain
from matrxs.agents.patrolling_agent import PatrollingAgentBrain
from matrxs.world_builder import WorldBuilder


def create_factory():
    factory = WorldBuilder(shape=[22, 10])

    human_agent = HumanAgentBrain()
    autonomous_agent = PatrollingAgentBrain(waypoints=[(0, 0), (0, 7)])

    usrinp_action_map = {
        'w': MoveNorth.__name__,
        'd': MoveEast.__name__,
        's': MoveSouth.__name__,
        'a': MoveWest.__name__,
    }

    factory.add_human_agent([1, 1], human_agent, name="Henry",
                            usrinp_action_map=usrinp_action_map, visualize_shape='img',
                            img_name="civilian.png")
    factory.add_agent([0, 0], autonomous_agent, name="Bot",
                      visualize_shape='img', has_menu=True, img_name="explorervehicle.png")

    return factory
