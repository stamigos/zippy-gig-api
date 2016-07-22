from flask import jsonify
from zippy_gig import app
from zippy_gig.models import Account


@app.route("/")
def root():
    account = Account.get(id=1)
    return jsonify({"user": account.get_data()})
