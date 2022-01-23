from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import json
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)
app.config["SECRET_KEY"] = "004f2af45d3a4e161a7dd2d17fdae47f"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
basedir = os.path.abspath(os.path.dirname(__file__))


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')


# Init db
db = SQLAlchemy(app)


# Init ma
ma = Marshmallow(app)


# import and register resources from endpoint
from endpoint.users.resource import *
from endpoint.transactions.resource import *


# run server
if __name__ == '__main__':
    app.run(debug=True)