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

class Radar(EnvObject):

    def __init__(self, location, name="Radar"):
        """
        An object which represents a radar which can map a wide area (hypothetically).
        In reality does nothing.
        """
        super().__init__(name=name, location=location, visualize_colour="#000000",
                         visualize_shape=0, is_traversable=False, class_callable=Radar)

class AA_gun(EnvObject):

    def __init__(self, location, name="AA_gun"):
        """
        An object which represents a Anti-Aircraft gun which can shoot down
        flying agents in its vicinity (hypothetically).
        In reality does nothing.
        """
        super().__init__(name=name, location=location, visualize_colour="#000000",
                         visualize_shape=0, is_traversable=False, class_callable=AA_gun)

class VIP_inbound_notification(EnvObject):

    def __init__(self, location, name="VIP_inbound_notification", visualize_depth=None,
            visualize_size=1.0):
        """
        An object which represents a Anti-Aircraft gun which can shoot down
        flying agents in its vicinity (hypothetically).
        In reality does nothing.
        """
        super().__init__(name=name, location=location, visualize_colour="#ffff00",
                         visualize_shape=2, is_traversable=True,
                         class_callable=VIP_inbound_notification, visualize_depth=visualize_depth,
                         visualize_size=visualize_size)
