from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth

from httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_object('config')
app.debug = True
# cors = CORS(app, resources={r"/": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app)
# app.session_interface = RedisSessionInterface()
basic_auth = HTTPTokenAuth(scheme='Token')

from zippy_gig.auth import auth
from zippy_gig.client import client
from zippy_gig.error import error

app.register_blueprint(auth)
app.register_blueprint(client)
app.register_blueprint(error)




