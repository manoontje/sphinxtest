from matrxs.utils.utils import get_default_value
from matrxs.utils.utils import next_obj_id, get_inheritence_path


class EnvObject:
    """
    The basic class for all objects in the world.
    """

    def __init__(self, location, name, class_callable, customizable_properties=None,
                 is_traversable=None, is_movable=None,
                 visualize_size=None, visualize_shape=None, visualize_colour=None, visualize_depth=None,
                 visualize_opacity=None, **custom_properties):
        """
        The basic class for all objects in the world. This includes the AgentAvatar. All objects that are added to the
        GridWorld should inherit this class.

        An EnvObject always needs a location and a name. Since we have no idea where you want to put the object or how
        you want to call it.

        In addition agents may alter properties of objects, but only if they are specifically told to be customizable.
        This is done by providing a list of property names in the customizable_properties list.
        Any custom property is allowed to be customizable if in that list, but any keyword argument (e.g.
        is_traversable) may only be influenced by an Action indirectly. For example, the is_traversable property cannot
        be changed in any way, whereas the location property can only be changed indirectly through the PickUpObject
        action.

        A few properties are mandatory for the GridWorld, some Actions and the Visualizer to function. These are
        keyword arguments (e.g. is_traversable). If these are not set, they are obtained from the defaults.json file.

        This class specific allows you to create any object you desire that only differs in the properties it holds. For
        example both a simple block or complex object such as a 'fire' can be modeled with this class. They only differ
        in their mandatory and custom properties (a block is simply a colored square, whereas a 'fire' has potentially
        many more properties). In such a case you simply provide more keyword arguments to the constructor, these
        are automatically added to the self.custom_attributes dictionary. Allowing you to intuitively extend the
        properties of any EnvObject.

        If you want an object that can be altered by an action in a specific way, you can create it as long as it
        inherits from this class. For example the Door object is such an example which has a unique method that 'opens'
        or 'closes' the door. Which is called by the OpenDoor and CloseDoor actions.

        If you want an object that needs to update some of its own properties during the simulation, you can again
        create your own object as long as it inherits from this class. Then you can implement the update_properties
        method. The Battery object is such an example, which simply decreases its energy level property each time step.

        If you have a specific object you need to create a lot and you do not want to keep on setting every property
        every time for the custom_properties, you can make your own class again which must inherit from this class and
        only implement its constructor where these custom properties are set with your default value
        of choosing.

        :param name: String. Mandatory. The name of object, does not need to be unique.
        :param location: List or tuple of length two. Mandatory. The location of the object in the grid world.
        :param customizable_properties: List. Optional, default obtained from defaults.json. The list of attribute names
        that can be customized by other objects (including AgentAvatars and as an extension any Agent).
        :param is_traversable: Boolean. Optional, default obtained from defaults.json. Signals whether other objects can
        be placed on top of this object.
        :param carried_by: List. Optional, default obtained from defaults.json. A list of who is carrying this object.
        :param class_callable: Callable class. Optional, defaults to EnvObject. This is required to make a distinction
        between what kind of object is actually seen or visualized. The last element is always the lowest level class,
        whereas the first element is always EnvObject and everything in between are potential other classes in the
        inheritance chain.
        :param visualize_size: Float. Optional, default obtained from defaults.json. A visualization property used by
        the Visualizer. Denotes the size of the object, its unit is a single grid square in the visualization (e.g. a
        value of 0.5 is half of a square, object is in the center, a value of 2 is twice the square's size centered on
        its location.)
        :param visualize_shape: Int. Optional, default obtained from defaults.json. A visualization property used by the
        Visualizer. Denotes the shape of the object in the visualization. 0=Rectangle, 1=Triangle, 2=Circle
        :param visualize_colour: Hexcode string. Optional, default obtained from defaults.json. A visualization property
        used by the Visualizer. Denotes the colour of the object in visualization.
        :param visualize_depth: Integer. Optional, default obtained from defaults.json. A visualization property that
        is used by the Visualizer to draw objects in layers.
        :param visualize_opacity: Integer. Opacity of the object. From 0.0 to 1.0.
        :param **custom_properties: Optional. Any other keyword arguments. All these are treated as custom attributes.
        For example the property 'heat'=2.4 of an EnvObject representing a fire.
        """

        # Set the object's name.
        self.obj_name = name

        # Obtain a unique ID based on a global object counter, if not already set as an attribute in a super class
        if not hasattr(self, "obj_id"):
            self.obj_id = f"{self.obj_name}_{next_obj_id()}"

        # Make customizable_properties mutable if not given.
        if customizable_properties is None:
            self.customizable_properties = {}
        else:
            self.customizable_properties = customizable_properties

        # Set the class trace based on the given callable class object. This is required to make a distinction between
        # what kind of object is actually seen or visualized. The last element is always the lowest level class Object,
        # with the second last element being EnvObject. Any elements before that are custom EnvObject class names.
        self.class_inheritance = get_inheritence_path(class_callable)

        # Load defaults if not given. We do this loading this low-level (instead of for example in the WorldFactory) for
        # users to make it easier to build/extend their own WorldFactory and this way they do not have to deal with this
        # It also helps if users want to create a GridWorld without using the WorldFactory.
        if is_traversable is None:
            is_traversable = get_default_value(class_name="EnvObject", property_name="is_traversable")
        if visualize_size is None:
            visualize_size = get_default_value(class_name="EnvObject", property_name="visualize_size")
        if visualize_shape is None:
            visualize_shape = get_default_value(class_name="EnvObject", property_name="visualize_shape")
        if visualize_colour is None:
            visualize_colour = get_default_value(class_name="EnvObject", property_name="visualize_colour")
        if visualize_opacity is None:
            visualize_opacity = get_default_value(class_name="EnvObject", property_name="visualize_opacity")
        if visualize_depth is None:
            visualize_depth = get_default_value(class_name="EnvObject", property_name="visualize_depth")
        if is_movable is None:
            is_movable = get_default_value(class_name="EnvObject", property_name="is_movable")

        # Set the mandatory properties
        self.visualize_depth = visualize_depth
        self.visualize_colour = visualize_colour
        self.visualize_opacity = visualize_opacity
        self.visualize_shape = visualize_shape
        self.visualize_size = visualize_size
        self.is_traversable = is_traversable
        self.is_movable = is_movable

        # Since carried_by cannot be defined beforehand (it contains the unique id's of objects that carry this object)
        # we set it to an empty list by default.
        self.carried_by = []

        # Go through the custom properties that were given (if any) and set them to the custom_properties dictionary
        self.custom_properties = {}
        for k, v in custom_properties.items():
            self.custom_properties[k] = v

        # location should be set at the end (due to the dependency of its setter on the other properties (e.g. in
        # AgentAvatar)
        self.location = location

    def update(self, grid_world):
        """
        Used to update some properties of this object if needed. For example a 'status' property that changes over time.
        It can also be used to update something in the GridWorld. For example a Fire object that damages other objects
        in its location.

        If you want this functionality, you should create a new object that inherits from this class EnvObject.

        This method is called automatically in the game-loop inside a running GridWorld instance.

        Parameters
        ----------
        grid_world
            The GridWorld instance representing the entire grid world. Can be used to alter itself or others in the
            world in some way.
        """
        pass

    def change_property(self, property_name, property_value):
        """
        Changes the value of an existing (!) property.
        :param property_name: The name of the property.
        :param property_value:  The value of the property.
        :return: The new properties.
        """

        # We check if it is a custom property and if so change it simply in the dictionary
        if property_name in self.customizable_properties:
            self.custom_properties[property_name] = property_value
        else:  # else we need to check if property_name is a mandatory class attribute that is also a property
            if property_name == "is_traversable":
                assert isinstance(property_value, bool)
                self.is_traversable = property_value
            elif property_name == "name":
                assert isinstance(property_value, str)
                self.obj_name = property_value
            elif property_name == "location":
                assert isinstance(property_value, list) or isinstance(property_value, tuple)
                self.location = property_value
            elif property_name == "class_inheritance":
                assert isinstance(property_value, list)
                self.class_inheritance = property_value
            elif property_name == "visualize_size":
                assert isinstance(property_value, int)
                self.visualize_size = property_value
            elif property_name == "visualize_colour":
                assert isinstance(property_value, str)
                self.visualize_colour = property_value
            elif property_name == "visualize_opacity":
                assert isinstance(property_value, float)
                self.visualize_opacity = property_value
            elif property_name == "visualize_shape":
                assert isinstance(property_value, int)
                self.visualize_shape = property_value
            elif property_name == "visualize_depth":
                assert isinstance(property_value, int)
                self.visualize_depth = property_value
            elif property_name == "is_movable":
                assert isinstance(property_value, bool)
                self.is_movable = property_value

        return self.properties

    def add_property(self, property_name, property_value):
        """
        Adds a new(!) property with its value to the object.
        """
        if property_name in self.custom_properties:
            raise Exception("Attribute already exists, alter value with change_property instead")
        else:
            # We always add it as a custom property which is also customizable (since we can add it)
            self.custom_properties[property_name] = property_value
            self.customizable_properties.append(property_name)

    @property
    def location(self):
        """
        The location of any object is a pythonic property, this allows us to do various checks on it. One of them is the
        setter that is overridden in AgentAvatar to also transfer all carried objects with it.
        :return: The current location as a tuple; (x, y)
        """
        return tuple(self.__location)

    @location.setter
    def location(self, loc):
        """
        The setter than can be overridden if a location change might also affect some other things inside the
        EnvObject (such as in the case of an AgentAvatar; all the objects its holding change their locations as well).
        :param loc: The new location
        """
        assert isinstance(loc, list) or isinstance(loc, tuple)
        assert len(loc) == 2
        self.__location = loc

    @property
    def properties(self):
        """
        Returns the custom properties of this object, but also any mandatory properties such as location, name,
        is_traversable and all visualization properties (those are in their own dictionary under 'visualization').

        In the case we return the properties of a class that inherits from EnvObject, we check if that class has

        :return: All mandatory and custom properties in a dictionary.
        """

        # Copy the custom properties
        properties = self.custom_properties.copy()

        # Add all mandatory properties. Make sure that these are updated if one are added to the constructor!
        properties['name'] = self.obj_name
        properties['obj_id'] = self.obj_id  # we return id as well, but this should never ever be modified!
        properties['location'] = self.location
        properties['is_movable'] = self.is_movable
        properties['carried_by'] = self.carried_by
        properties['is_traversable'] = self.is_traversable
        properties['class_inheritance'] = self.class_inheritance
        properties['visualization'] = {
            "size": self.visualize_size,
            "shape": self.visualize_shape,
            "colour": self.visualize_colour,
            "depth": self.visualize_depth,
            "opacity": self.visualize_opacity
        }

        return properties

    @properties.setter
    def properties(self, property_dictionary: dict):
        """
        Here to protect the 'properties' variable. It does not do anything and should not do anything!
        """
        pass
