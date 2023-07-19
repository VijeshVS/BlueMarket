from bluemarket import app
from flask import render_template , redirect , url_for , flash , get_flashed_messages
from bluemarket.models import Item , User
from bluemarket.forms import RegisterForm , LoginForm
from bluemarket import db
from flask_login import login_user , logout_user , login_required

# importing the required libaries ----------->

@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/items")
@login_required
def item_page():
    items = Item.query.all() # retreiving all the objects from the Database from a table named Item and storing  
                             # it to a variable and passing all the objects to the items.html file
    return render_template("items.html", items=items)



'''
here we are creating the instance of register form (mentioned in forms.py)
and creating the User instance on Submit

Post and Get --->
Post request is something when we click on submit the data is sent as post
request to the server
Get request is retreiving data means when we visit a website its nothing but get request

damn!! if no method request is specified it by default uses the GET method
to retrieve the info from the html page 
'''
@app.route('/register' , methods=['POST','GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
                              username =form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data
                              ) 
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully ! Now you are logged in as {user_to_create.username}', category='success')
        return redirect(url_for('item_page'))
    


    '''
    checking if the there is errors or not .
    Form errors are simple stored in dictionaries and we need to iterate 
    through to get the value
    '''

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash (f'There was an error while creating the user {err_msg}' , category='danger')      
    return render_template('register.html' , form=form)


@app.route('/login', methods = ['GET','POST'])

def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category = 'success')
            return redirect(url_for('item_page'))
        else:
            flash('Username or password is incorrect ! Please try again', category='danger')

    return render_template('login.html',form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'Successfully logged out !', category = 'info')
    return redirect(url_for('home_page'))