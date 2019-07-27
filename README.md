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

# Context variables:
see constraint learning repository

# Installation
`pip3 install -r requirements.txt`

# Runing the code

## running the experiment
- from the root of the repository, run: `python3 start_experiment.py`
- This will start the experiment introduction, at ...




## Only running the simulator (MATRXS)
- in `cl_main.py`, define a scenario number (between 0 and 126)
- `python3 cl_main.py`
- Go to `localhost:3000/god` to see the simulation run
