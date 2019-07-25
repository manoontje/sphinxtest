from scenarios.cl_scenarios import sc_from_contexts as sc

if __name__ == "__main__":

    fl = "../tasking-constraint-learning/demo_dataset/v2/contexts.csv"

    # Used as example of commander user interface
    factory = sc.create_factory(file=fl, scenario_n=79)




    # factory = sc.create_factory(file=fl, scenario_n=45)


    for world in factory.worlds():
        world.run()
