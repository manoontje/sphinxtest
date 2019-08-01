import demo

if __name__ == "__main__":

    # By creating scripts that return a factory, we can define infinite number of use cases and select them (in the
    # future) through a UI.
    builder = demo.create_builder()

    for world in builder.worlds():
        world.run()
