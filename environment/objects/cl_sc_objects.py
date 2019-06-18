from environment.objects.env_object import EnvObject
from scenario_manager.helper_functions import get_default_value

# 
# class Wall(EnvObject):
#
#     def __init__(self, location, name="Wall", visualization_colour="#000000"):
#         """
#         A simple Wall object. Is not traversable, the colour can be set but has otherwise the default EnvObject property
#         values.
#         :param location: The location of the wall.
#         :param name: The name, default "Wall".
#         """
#         is_traversable = False  # All walls are always not traversable
#         super().__init__(name=name, location=location, visualize_colour=visualization_colour,
#                          is_traversable=is_traversable, class_callable=Wall)
