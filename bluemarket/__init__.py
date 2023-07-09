from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"
app.config['SECRET_KEY'] = '46d41ac8259358fac094234d'

db = SQLAlchemy(app)
app.app_context().push()

from bluemarket import routes

