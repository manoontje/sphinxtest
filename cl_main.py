from scenarios.cl_scenarios import cl_sc4 as sc

if __name__ == "__main__":

    # By creating scripts that return a factory, we can define infinite number of use cases and select them (in the
    # future) through a UI.
    factory = sc.create_factory()

    for world in factory.worlds():
        world.run()
