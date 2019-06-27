from scenarios.cl_scenarios import cl_sc1, cl_sc2, cl_sc3, cl_sc4, cl_sc5, base_sc

if __name__ == "__main__":

    # By creating scripts that return a factory, we can define infinite number of use cases and select them (in the
    # future) through a UI.
    factory = base_sc.create_factory()

    for world in factory.worlds():
        world.run()
