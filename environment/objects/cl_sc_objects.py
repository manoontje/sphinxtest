from environment.objects.env_object import EnvObject
from scenario_manager.helper_functions import get_default_value


class HouseBase(EnvObject):

    def __init__(self, location, name="HouseBase", visualize_colour="#000000"):
        """
        A simple Square object representing a house. Is always traversable
        :param location: The location of the wall.
        :param name: The name, default "Wall".
        """
        super().__init__(name=name, location=location, visualize_colour=visualize_colour,
                         visualize_shape=0, is_traversable=True, class_callable=HouseBase)


class HouseRoof(EnvObject):

    def __init__(self, location, name="HouseRoof", visualize_colour="#000000"):
        """
        A simple Square object representing a house. Is always traversable
        :param location: The location of the wall.
        :param name: The name, default "Wall".
        """
        super().__init__(name=name, location=location, visualize_colour=visualize_colour,
                         visualize_shape=1, is_traversable=True, class_callable=HouseRoof)


class Water(EnvObject):

    def __init__(self, location, name="Water", visualize_colour="#024a74"):
        """
        A simple Square object representing a house. Is always traversable
        :param location: The location of the wall.
        :param name: The name, default "Wall".
        """
        super().__init__(name=name, location=location, visualize_colour=visualize_colour,
                         visualize_shape=0, is_traversable=True, class_callable=Water)
