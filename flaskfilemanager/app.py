from flask import Flask
import flaskfilemanager

# Create the webapp
app = Flask(__name__)

# This is where the path for the uploads is defined
app.config['FLASKFILEMANAGER_FILE_PATH'] = 'tmp-webapp-uploads'

# You'll obviously do some more Flask stuff here!

# Initialise the filemanager
flaskfilemanager.init(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
