google-chrome file:///home/tjalling/Projects/tasking-constraint-learning/experiment/tutorial/intro.html
cd ~/Projects/matrxs/visualization
python3.6 server.py &
google-chrome http://localhost:3000/god &
cd ~/Projects/matrxs/
export FLASK_APP=run_experiment.py
flask run -p 3001 & 
google-chrome http://localhost:3001 &


