from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from zippy_gig.utils import JSONEncoder
from httpauth import HTTPBasicAuth
from zippy_gig.admin import AccountAdmin
from zippy_gig.models import Account

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='admin/templates')
app.config.from_object('config')
app.debug = True
app.json_encoder = JSONEncoder
admin = Admin(app, name='Zippy Gigs Admin', template_mode='bootstrap3')
admin.add_view(AccountAdmin(Account))

# CORS(app)
# cors = CORS(app, resources={r"/": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app)
# app.session_interface = RedisSessionInterface()
token_auth = HTTPBasicAuth(scheme="Token")
# token_auth = HTTPTokenAuth(scheme='Token')

from zippy_gig.auth import auth
from zippy_gig.client import client
from zippy_gig.error import error
from zippy_gig.gig import gig
from zippy_gig.vendor import vendor

app.register_blueprint(auth)
app.register_blueprint(client)
app.register_blueprint(error)
app.register_blueprint(gig)
app.register_blueprint(vendor)
