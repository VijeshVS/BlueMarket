from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"

db = SQLAlchemy(app)
app.app_context().push()


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f"Item {self.name}"


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/items")
def item_page():
    items = Item.query.all()
    return render_template("items.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)
