from bluemarket import app
from flask import render_template , redirect , url_for , flash , get_flashed_messages
from bluemarket.models import Item , User
from bluemarket.forms import RegisterForm
from bluemarket import db

# importing the required libaries ----------->

@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/items")
def item_page():
    items = Item.query.all() # retreiving all the objects from the Database from a table named Item and storing  
                             # it to a variable and passing all the objects to the items.html file
    return render_template("items.html", items=items)


@app.route('/register' , methods=['POST','GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
                              username =form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data
                              )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('item_page'))

    #checking if the there is errors or not . Form errors are simple stored in dictionaries and we need to iterate 
    # through to get the value

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash (f'There was an error while creating the user {err_msg}')      
    return render_template('register.html' , form=form)
