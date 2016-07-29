import sys, os
import site
sys.path.insert (0,'/var/www/zippy-gig')
os.chdir("/var/www/zippy-gig")

import logging
logging.basicConfig(stream=sys.stderr)

# Install venv by `virtualenv --distribute venv`
# Then install depedencies: `source venv/bin/active`
# `pip install -r requirements.txt`
activate_this = '/home/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

path = os.path.join(os.path.dirname(__file__), os.pardir)
if path not in sys.path:
    sys.path.append(path)

# The application object is used by any WSGI server configured to use this
# file.

# Ensure there is an app.py script in the current folder
from zippy_gig import app as application
