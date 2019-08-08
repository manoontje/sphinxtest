from flask import Flask, flash, request, render_template, jsonify, redirect
from flask_socketio import socketio
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import Required, InputRequired, DataRequired, Optional
import pandas as pd

# relative import pointing to parent folder
from sim import create_world

'''
Teaching User Interface
'''


app = Flask(__name__, template_folder='teaching_UI/static/templates')
app.config['SECRET_KEY'] = 'secret!'

# config file has STATIC_FOLDER='/core/static'
app.static_url_path = "/teaching_UI/static/"

# set the absolute path to the static folder
app.static_folder = app.root_path + app.static_url_path

# name of file in which to save user data
subject_name = "anne"
# path to save user data to
folder_path = "../tasking-constraint-learning/demo_dataset/user_data/"

# These are the constraints used, if you want to change this, also change the fields
# in the form below
constraint_names = ["time_limit", "flying_speed", "update_freq", "fly_village", "fly_water", "tank_dist", "radar_dist"]

# the file with scenarios in randomized order
contexts_fl = "../tasking-constraint-learning/demo_dataset/scenarios/contexts_randomized.csv"



# constraints form
class constraintsForm(FlaskForm):

    time_limit = RadioField('Time limit:',
            choices=[('short','Short'),('long','Long'), ('None','None')])

    flying_speed = RadioField('Drone flying speed:',
            choices=[('slow','Slow'), ('fast','Fast')])

    update_freq = RadioField('Drone notifcation frequency with mission updates:',
            choices=[('low','Low'), ('high','High')])

    fly_village = RadioField('Prohibit flying over the village:',
            choices=[('no','No'), ('yes','Yes')])

    fly_water = RadioField('Prohibit flying over water:',
            choices=[('no','No'), ('yes','Yes')])

    tank_dist = RadioField('Minimum distance to tank:',
            choices=[('low','Low'), ('high','High')], validators=[Optional()])

    radar_dist = RadioField('Minimum distance to radar:',
            choices=[('low','Low'), ('high','High')], validators=[Optional()])

    submit = SubmitField('Next')


# redirect to the first experiment
@app.route('/')
def start():
    return redirect('/1')


# the teaching interface with the constraints form, for a specific trial
@app.route('/<int:trial>', methods=['GET', 'POST'])
def teaching_UI(trial):

    # create scenario and run simulation for 1 tick
    create_world(scenario_n=trial-1, contexts_file=contexts_fl)
    settings = fetch_settings(contexts_fl, trial-1)

    # create user constraints form
    consForm = constraintsForm()

    # check if this page was received form data
    if consForm.validate_on_submit():
        print(f'Trial {trial}. Form submitted with data')
        write_result_to_csv(consForm, trial)
        return redirect('/' + str(trial + 1))

    if consForm.errors != {}:
        print("Form errors:", consForm.errors)

    return render_template('teaching_UI.html', trial=trial, form=consForm,
            tank=settings['intel_anti-air_at_x'], radar=settings['intel_radar_at_x'])




def write_result_to_csv(form, trial):
    '''
    Write the constraints specified by the user for a specific trial to a csv file
    '''

    # create and open file
    fl = folder_path + subject_name + ".csv"
    mode = 'w' if trial == 1 else 'a+'
    with open(fl, mode) as f:

        # add constraint names / headers if it is the first trial
        if trial == 1:
            f.write(",".join(constraint_names) + "\n")

        # get form data
        usr_constraints = f"{form.time_limit.data}, {form.flying_speed.data}, \
                            {form.update_freq.data}, {form.fly_village.data}, \
                            {form.fly_water.data}, {form.tank_dist.data}, \
                            {form.radar_dist.data}"

        # write to file
        f.write(f"{usr_constraints.replace(' ','')}\n")
        print(f"Appended trial {trial} data to {fl}\n")




def fetch_settings(fl, scenario_n):
    ''' read in data of that specific scenario '''
    df = pd.read_csv(fl)
    settings = df.iloc[scenario_n,:]
    return settings



if __name__ == "__main__":
    print("Server running")
    socketio.run(app, port=3001)
