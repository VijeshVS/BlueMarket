from bluemarket import app
from flask import render_template
from bluemarket.models import Item

@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/items")
def item_page():
    items = Item.query.all()
    return render_template("items.html", items=items)