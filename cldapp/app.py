"""
App factory function
"""

import logging
import datetime
import traceback
import os.path
import subprocess, os
global TARGETPATH, LISTENPORT
TARGETPATH = str(subprocess.Popen('for OPTS in $(ps ax | grep '+str(os.getpid())+');do echo $OPTS | grep -q  "\-\-targetpath=" && echo $OPTS | cut -d = -f 2;done', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=256*1024*1024).communicate()[0].decode('utf8').replace('\n', ''))
LISTENPORT = int(subprocess.Popen('for OPTS in $(ps ax | grep '+str(os.getpid())+');do echo $OPTS | grep -q  "\-\-listenport=" && echo $OPTS | cut -d = -f 2;done', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=256*1024*1024).communicate()[0].decode('utf8').replace('\n', ''))
#print(TARGETPATH)
from flask import Flask, render_template
import jinja2
from littlefish import timetool
import flaskfilemanager

from main import main

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

CACHE_BUSTER = int(timetool.unix_time())

log = logging.getLogger(__name__)


logging.basicConfig(level=logging.DEBUG)

# Create the webapp
app = Flask(__name__)
app.secret_key = 'TestAppSecretKeyWhoCaresWhatThisIs'
app.config['TEMPLATES_AUTO_RELOAD'] = True
# This is where the path for the uploads is defined
app.config['FLASKFILEMANAGER_FILE_PATH'] = TARGETPATH
#app.config['FLASKFILEMANAGER_FILE_PATH'] = '/root/'
try:
    app.config.from_object('config')
    log.info('Local config loaded')
except Exception:
    log.info('Config not found or invalid')

# Don't allow output of undefined variables in jinja templates
app.jinja_env.undefined = jinja2.StrictUndefined

log.info('Registering blueprints')
app.register_blueprint(main)

# Initialise the filemanager
log.info('Initialising filemanager')
config_json_path = os.path.join(app.root_path, 'static/js/filemanager.config.json')
init_js_path = os.path.join(app.root_path, 'static/js/filemanager.init.js')
flaskfilemanager.init(app, custom_config_json_path=config_json_path, custom_init_js_path=init_js_path)

@app.context_processor
def add_global_context():
    return {
        'date': datetime.datetime.now(),
        'CACHE_BUSTER': CACHE_BUSTER
    }

@app.errorhandler(Exception)
def catch_all(e):
    title = str(e)
    message = traceback.format_exc()

    log.error('Exception caught: %s\n%s' % (title, message))

    return render_template('error_page.html', title=title, message=message, preformat=True)

if __name__ == "__main__":
     app.run(debug=True, host='172.17.0.250', port=LISTENPORT)
