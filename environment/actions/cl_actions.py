import numpy as np
import collections, math

from environment.actions.action import Action, ActionResult
from environment.objects.agent_avatar import AgentAvatar
from environment.objects.simple_objects import AreaTile
import copy


class DeclareAreaChecked(Action):
    """
    Action which can be executed after performing surveillance on an area, as
    to declare surveillance of the area complete (and change the colour of the target
    area)
    """

    def __init__(self):
        name = DeclareAreaChecked.__name__
        super().__init__(name)


    def mutate(self, grid_world, agent_id, **kwargs):


        # change the colour of the 5 target area objects
        for obj_ID, obj in grid_world.environment_objects.items():
            if 'target_area' in obj_ID:
                obj.visualize_colour = "#00FF00"

        return DACActionResult(DACActionResult.ACTION_SUCCEEDED, True)



    def is_possible(self, grid_world, agent_id, **kwargs):

        # check if the 5 target_area objects exist
        target_area_ids = []
        for obj in grid_world.environment_objects:
            if 'target_area' in obj:
                target_area_ids.append(obj)

        if len(target_area_ids) == 5:
            return True, DACActionResult(DACActionResult.ACTION_SUCCEEDED, True)
        else:
            return True, DACActionResult(DACActionResult.TARGET_NOT_FOUND, True)



class DACActionResult(ActionResult):
    """ Action result for DeclareAreaChecked action """
    TARGET_NOT_FOUND = "One or multiple of the 5 objects with names containing 'target_area' could not be found"
    ACTION_SUCCEEDED = "DeclareAreaChecked action succesfully completed."

    def __init__(self, result, succeeded):
        super().__init__(result, succeeded)
