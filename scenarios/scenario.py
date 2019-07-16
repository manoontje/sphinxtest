class Scenario:

    def __init__(self):
        pass

    def create_factory(self):
        return WorldFactory(random_seed=1, shape=[10, 10], tick_duration=0.5) 
