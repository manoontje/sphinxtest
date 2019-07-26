from flask import Flask, flash, request, render_template, jsonify, redirect
from flask_socketio import socketio
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import Required, InputRequired, DataRequired

'''
Teaching User Interface
'''


app = Flask(__name__, template_folder='static/templates')
app.config['SECRET_KEY'] = 'secret!'

debug = False



# constraints form
class constraintsForm(FlaskForm):

    time_limit = RadioField('Time limit:',
            choices=[('short','Short'),('long','Long'), ('None','None')])

    flying_speed = RadioField('Drone flying speed:',
            choices=[('slow','Slow'), ('fast','Fast')])

    update_freq = RadioField('Frequency of sending updates:',
            choices=[('low','Low'), ('high','High')])

    fly_village = RadioField('People min distance:',
            choices=[('low','Low'), ('high','High')])

    fly_water = RadioField('Prohibit flying over water:',
            choices=[('no','No'), ('yes','Yes')])

    tank_dist = RadioField('Minimum distance to tank:',
            choices=[('low','Low'), ('high','High')])

    radar_dist = RadioField('Minimum distance to radar:',
            choices=[('low','Low'), ('high','High')])

    submit = SubmitField('Next')


# redirect to the first experiment
@app.route('/')
def start():
    return redirect('/1')


# the teaching interface with the constraints form for experiment number x
@app.route('/<trial>', methods=['GET', 'POST'])
def teaching_UI(trial):
    # create form
    consForm = constraintsForm()

    # received form data
    if consForm.validate_on_submit():
        print('Form submitted with data')
        return redirect('/' + str(int(trial) + 1))

    if consForm.errors != {}:
        print("Form errors:", consForm.errors)

    return render_template('teaching_UI.html', trial=trial, form=consForm)



if __name__ == "__main__":
    print("Server running")
    socketio.run(app, port=3001)
