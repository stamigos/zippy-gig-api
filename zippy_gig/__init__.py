from flask import Flask

from httpauth import HTTPBasicAuth
from redis_sessions import RedisSessionInterface

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_object('config')
# app.session_interface = RedisSessionInterface()
basic_auth = HTTPBasicAuth()

from zippy_gig.auth import auth
from zippy_gig.client import client
from zippy_gig.error import error

app.register_blueprint(auth)
app.register_blueprint(client)
app.register_blueprint(error)



