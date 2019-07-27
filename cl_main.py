from scenarios.cl_scenarios import sc_from_contexts as sc

if __name__ == "__main__":

    # file with all the possible scenarios (consisting of context variables)
    fl = "../tasking-constraint-learning/demo_dataset/gen/contexts.csv"

    # Used as example of commander user interface
    factory = sc.create_factory(file=fl, scenario_n=111)


    # factory = sc.create_factory(file=fl, scenario_n=45)


    for world in factory.worlds():
        world.run()
