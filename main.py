import test_scenario
import scenario_manon

if __name__ == "__main__":

    # By creating scripts that return a factory, we can define infinite number of use cases and select them (in the
    # future) through a UI.
    # factory = test_scenario.create_factory()
    factory = scenario_manon.create_factory()

    for world in factory.worlds(nr_of_worlds=1):
        world.run()
