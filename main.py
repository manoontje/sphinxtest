from blanket_search.scenarios import scenario1
from scenarios import sc_from_contexts as sc

if __name__ == "__main__":

    # By creating scripts that return a factory, we can define infinite number of use cases and select them (in the
    # future) through a UI.
    factory = sc(10).create_factory()



    for world in factory.worlds():
        world.run()
