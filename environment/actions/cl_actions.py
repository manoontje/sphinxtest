import numpy as np
import collections, math
from colour import Color as Colour

from environment.actions.action import Action, ActionResult
from environment.objects.simple_objects import AreaTile
from environment.objects.cl_sc_objects import Water
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



class StirWater(Action):
    """
    Action which which stirs all the water in the scenario
    by changing its colour. E.g. because of winds.
    """

    def __init__(self):
        name = StirWater.__name__
        super().__init__(name)

        dark_clr="#024a74"
        light_clr="#6c9cb5"
        groundClr = Colour(dark_clr)
        # create a gradient from light to dark colours
        self.lake_colours = list(groundClr.range_to(Colour(light_clr), 10))
        self.water_change_prob = 0.05

    def mutate(self, grid_world, agent_id, **kwargs):

        waterObjs = grid_world.get_objects_in_range(agent_loc=[0,0], object_type=Water, sense_range=np.inf)

        # set new colour for water
        for ID, waterObj in waterObjs.items():
            # randomly determine if this specific blob of water will change
            if np.random.random_sample() > self.water_change_prob:
                waterObj.visualize_colour = np.random.choice(self.lake_colours).hex

        return StirWaterActionResult(DACActionResult.ACTION_SUCCEEDED, True)



    def is_possible(self, grid_world, agent_id, **kwargs):
        # check if there is any water present in this scenario
        waterObjs = grid_world.get_objects_in_range(agent_loc=[0,0], object_type=Water, sense_range=np.inf)

        if len(waterObjs) > 0:
            return True, StirWaterActionResult(StirWaterActionResult.ACTION_SUCCEEDED, True)
        else:
            return True, StirWaterActionResult(StirWaterActionResult.TARGET_NOT_FOUND, True)



class StirWaterActionResult(ActionResult):
    """ Action result for DeclareAreaChecked action """
    TARGET_NOT_FOUND = "There is no water in this scenario."
    ACTION_SUCCEEDED = "StirWater action succesfully completed."

    def __init__(self, result, succeeded):
        super().__init__(result, succeeded)
