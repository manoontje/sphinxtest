from environment.objects.env_object import EnvObject
from world_factory.helper_functions import get_default_value
from colour import Color as Colour
import numpy as np

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
        dark_clr="#024a74"
        light_clr="#6c9cb5"
        groundClr = Colour(dark_clr)
        lake_colours = list(groundClr.range_to(Colour(light_clr), 10))
        visualize_colour = np.random.choice(lake_colours).hex

        print(visualize_colour)

        super().__init__(name=name, location=location, visualize_colour=visualize_colour,
                         visualize_shape=0, is_traversable=True, class_callable=Water)

class Radar(EnvObject):

    def __init__(self, location, visualize_shape=0, visualize_size=1.0,
            name="Radar", img_name=None, visualize_depth=100):
        """
        An object which represents a radar which can map a wide area (hypothetically).
        In reality does nothing.
        """
        custom_properties = {}
        if img_name is not None:
            custom_properties['img_name'] = img_name
        super().__init__(name=name, location=location, visualize_colour="#000000",
                         visualize_shape=visualize_shape, is_traversable=False,
                         class_callable=Radar, visualize_size=visualize_size,
                         visualize_depth=visualize_depth, **custom_properties)

class AA_gun(EnvObject):

    def __init__(self, location, visualize_shape=0, visualize_size=1.0,
            name="AA_gun", img_name=None, visualize_depth=100):
        """
        An object which represents a Anti-Aircraft gun which can shoot down
        flying agents in its vicinity (hypothetically).
        In reality does nothing.
        """
        custom_properties = {}
        if img_name is not None:
            custom_properties['img_name'] = img_name
        super().__init__(name=name, location=location, visualize_colour="#000000",
                          is_traversable=False, class_callable=AA_gun,
                         visualize_shape=visualize_shape, visualize_size=visualize_size,
                         visualize_depth=visualize_depth, **custom_properties)

class VIP_inbound_notification(EnvObject):

    def __init__(self, location, name="VIP_inbound_notification", visualize_depth=None,
            visualize_size=1.0, visualize_shape=2, img_name=None):
        """
        An object which represents a Anti-Aircraft gun which can shoot down
        flying agents in its vicinity (hypothetically).
        In reality does nothing.
        """
        custom_properties = {}
        if img_name is not None:
            custom_properties['img_name'] = img_name

        print("Initializing VIP inbound notification with custom properties:", custom_properties)

        super().__init__(name=name, location=location, visualize_colour="#ffff00",
                         visualize_shape=visualize_shape, is_traversable=True,
                         class_callable=VIP_inbound_notification, visualize_depth=visualize_depth,
                         visualize_size=visualize_size, **custom_properties)
