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
- fly height instead of flight speed
- intel village not possible
- show contexts as text as well: daytime / weather (/ estimated_threat_env)

- human needs to know how to perform task to be consistent in instructions
    - Choose task already trained in?
    - trained human fills in constraints correctly -> drone learns
    - Do not have to know/specify what human intention is, as long as human is consistent.
        Goal is to see if it can be learned.

- Inspect learned drone behaviour, ask human for human intention / logic. Check with learned behaviour.

# aesthetics fixes
- wind vertically moving
- shark

# story
- You are a military commander located in an encampment in a foreign country (picture), You are in charge of keeping the area save. Current task is [...].

- To minimize danger to yourself, a drone has been provided for performing reconnaissance tasks.
- Secondly, a commander user interface which gives an overview of the situation, showing a visualization of the current situation, the location of the drone, and intelligence on locations of (incoming) friendlies or enemies.

- Previously this drone was manually controlled, but it took a lot of time. So at the moment, the military is experimenting with making it autonomous.
- As you are the expert, they ask you to first provide knowledge for the drone, so it can learn to perform
the task as you would have intended it.

- Examples of various situations you might encounter are:

    - Show different contexts:
        - Night time (/ day time )
        - Fog / heavy winds (/ clear)
        - intel_radar_at_x
        - intel VIP
        - intel_anti-air_at_x
        - Area type: urban / village + fast flying

- Provide knowledge through constraints:
    - Show possible constraints
