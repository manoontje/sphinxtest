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
- Requires python 3.6 or higher
- Run: `pip3 install -r requirements.txt`

# Runing the code

## running the experiment
- `cd visualization` and run `python3 server.py`
- open two internet browser screens (side by side)
- point browser 1 to the url `localhost:3000`. This is the simulator view.

- In `run_experiment.py`, specify the name of the test subject and the folder to write the results to.
- Open a second terminal in the root of the repository and run: `python3 run_experiment.py`
- in the second internet browser, go to `localhost:3001`. This view shows the constraints which the user can teach to the drone.

- The experiment will now begin and go through all scenarios in a random order. Data will be saved in a subject_name.csv file in the folder you specified.





## Only running the simulator (MATRXS)
- in `cl_main.py`, define a scenario number (between 0 and 126)
- `python3 cl_main.py`
- Go to `localhost:3000/god` to see the simulation run
