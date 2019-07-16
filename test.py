from scenarios import *
from environment.helper_functions import get_all_classes
# from scenarios import *



sc = get_all_classes(scenario.Scenario, omit_super_class=True)
print(sc)
