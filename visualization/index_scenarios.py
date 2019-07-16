from scenarios import *
from environment.helper_functions import get_all_classes


def get_all_scenarios(cl):

    return get_all_classes(scenario.Scenario, omit_super_class=True)
