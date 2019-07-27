from scenarios.cl_scenarios import sc_from_contexts as sc


def create_world(scenario_n, contexts_file):
    # file with all the possible scenarios (consisting of context variables)


    # Used as example of commander user interface
    factory = sc.create_factory(file=contexts_file, scenario_n=scenario_n, simulation_goal=1)


    # factory = sc.create_factory(file=fl, scenario_n=45)


    for world in factory.worlds():
        world.run()


if __name__ == "__main__":
    fl = "../tasking-constraint-learning/demo_dataset/gen/contexts_ordered.csv"
    create_world(111, fl)
