
import subprocess

# start teacher UI
# open chrome with link
# start visualization server
# open chrome with link

# start visualization server

subprocess.call('export FLASK_APP=teaching_UI/server.py')
subprocess.call('flask run -p 3001')
