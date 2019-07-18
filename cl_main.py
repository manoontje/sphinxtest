from scenarios.cl_scenarios import sc_from_contexts as sc

if __name__ == "__main__":

    fl = "../tasking-constraint-learning/demo_dataset/v2/contexts.csv"


    # By creating scripts that return a factory, we can define infinite number of use cases and select them (in the
    # future) through a UI.
    factory = sc.create_factory(file=fl, scenario_n=242)


    for world in factory.worlds():
        world.run()
