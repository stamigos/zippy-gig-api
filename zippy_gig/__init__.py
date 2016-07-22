from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_object('config')

from zippy_gig.auth import auth

app.register_blueprint(auth)


