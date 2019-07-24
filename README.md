# Testbed

2D-discrete testbed to facilitate HAT-research, with SAIL connection

For documentation see the wiki at [https://ci.tno.nl/gitlab/SAIL-framework/testbed/wikis/home](https://ci.tno.nl/gitlab/SAIL-framework/testbed/wikis/home).


# Constraint learning for taskable agents
A taskable agent which can learn the intention of the human on how the provided task task should be performed. As a approximation to human intention, constraints are used, at the start provided by the human. The agent tries to chracterize a scenario based on context variables, and learn the relation between these and the human task constraints, as to learn the human's intention.

### Changes compared to dev branch
- water object
- house objects + add_buildings function in WorldFactory
- custom agent with (simple) pathplanning
- some demo scenario's

### Future improvements
- enable a multi-tick movement animation in the visualization for slow movements. Now it is just a couple ticks of waiting, and then in 1 tick the animation/movement.

# Context variables:
see constraint learning repository

# conceptual fixes
- estimated_threat_env -> instead part of human thinking
- Removed heavy winds (no behaviour difference with fog)

# conceptual  issues
- should show contexts as text as well: daytime / weather / environment / intels
- should show constraints
- show task / priorities as well?
- add note to story: you won't see result of your actions.

- human needs to know how to perform task to be consistent in instructions
    - Approach 1
        - Let user think of context results themself
        - Do not have to know/specify what human intention is, as long as human is consistent.
            Goal is to see if it can be learned.
        - Let user perform test rounds
        - Afterwards, ask if anything changed, and so if what. Did AI learn this or not?
    - Approach 2:
        - Show context results
        - Let user perform test rounds
    - Approach 3
        - Choose task already trained in?
        - trained human fills in constraints correctly -> drone learns

- Inspect learned drone behaviour, ask human for human intention / logic. Check with learned behaviour.

# aesthetics fixes
- shark


# Experiments - Story
- You are a military commander located in an encampment in a foreign country (picture), You are in charge of keeping the area safe.
- To help you, you have been provided with the commander user interface, giving an overview of the situation. The Commander User Interface shows a visualization of the current environment, including information (intelligence) on locations of (incoming) friendlies or enemies etc.

- To minimize danger to yourself, a drone has been provided which can perform tasks for you, also marked on the map. Your current task is to use the drone to perform reconnaissance of the area marked with a cross, top right. If possible complete the task discretely (without being discovered by citizens or enemies). However, absolute priority is to not let the drone crash or be destroyed.

- Previously this drone was manually controlled but it took a lot of time. So now the military is experimenting with making it autonomous.
- By default the drone will take the shortest path to the area and do reconnaissance. However you, as the expert, know the shortest route does not always lead to the best result. As such the higher ups asked you to teach the drone how to do the task properly. You can do this by providing the drone with constraints on what it can and cannot do. E.g. in this situation fly slower, avoid this village, and set a time limit for the task.  
Note: Try to be consistent!

- Examples of various situations you might encounter are:

    - Show different contexts:
        - Night time (/ day time )
        - Fog (/ clear)
        - intel_radar_at_x
        - intel VIP:
        - intel_anti-air_at_x
        - intel_hostiles_in_village
        - Area type: Desert / Mountainous

## Possible explanation 1:
- Think shortly about each situation you see, and describe how you think it influences the task.
E.g., with fog the drone will crash more easily, so it should fly slower / prevent buildings.
Note: This helps you to be consistent!

## Possible explanation 2:
- Some examples from the result of these scenarios on the drone:
    - Fog:
        - Drone vision based, higher chance of crashing, e.g. when:
        - (Flying fast)
        - (Over water)
        - (Sudden winds from height differences (e.g. flying over village))
    - Tank:
        - Chance to detect and shoot down drone
        - (Flying close -> drone will be shot down!)
        - (Flying far -> safe)
    - Radar:
        - Chance to shoot down drone
        - (Flying close -> 50% chance of being detected!)
        - (Flying far -> safe)
    - VIP inbound:  
        - Have to be back in time for when VIP gets there --> pressed for time
        - (set time limit to break of task if it takes too long)
        - (flying slow will not make it in time back!)
    - night time:
        - Drone has lights, so you are more visible
        - (close to radar: detected for sure!)
        - (over village: 50% chance detected)
    - hostiles in village:
        - (flying over village: 50% chance shot down)
    - Mountainous (vs Urban / Desert):
        - Lower chance of being detected by radar, people and tank because of mountains


# Continuation Experiment

- You can provide knowledge to the drone via constraints.
    - Show possible constraints
    - [..]

- Test runs:
    - 10 or so test runs with context + constraints
    - Note: Try to be consistent!

- Real experiment. Do all scenarios in random order.
