from bluemarket import app
from flask import render_template , redirect , url_for , flash , get_flashed_messages , request
from bluemarket.models import Item , User , CouponData
from bluemarket.forms import RegisterForm , LoginForm , PurchaseItemForm , SellItemForm , RedeemCouponForm
from bluemarket import db
from flask_login import login_user , logout_user , login_required , current_user

# importing the required libaries ----------->

@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/items", methods = ['POST','GET'])
@login_required
def item_page():

    purchase_form = PurchaseItemForm()

    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()

        if current_user.buy_check(p_item_object):
            if p_item_object:
                p_item_object.onwer = current_user.id
                current_user.budget -= p_item_object.price
                flash(f"{purchased_item} is purchased successfully ! ", category='success')
                db.session.commit()
        else:
            flash(f'You do not have enough credits to buy {purchased_item}' , category='danger')

        return redirect(url_for('item_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(onwer = None) # retreiving all the objects from the Database from a table named Item and storing  
                             # it to a variable and passing all the objects to the items.html file
        return render_template("items.html", items=items,purchase_form=purchase_form)



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



@app.route('/myitems', methods = ['GET','POST'])
@login_required 
def myitem_page():   
    sellform = SellItemForm()
    
    if request.method == 'POST':
        item_name = request.form.get('sell_item')
        item_object = Item.query.filter_by(name = item_name).first()
        current_user.budget += item_object.price
        item_object.onwer = None
        db.session.commit()
        flash(f'{item_name} sold successfully for {item_object.price}$' , category='success')
        return redirect(url_for('myitem_page'))

    if request.method == 'GET':
        items  = Item.query.filter_by(onwer = current_user.id)
        return render_template('myitem.html' , items = items , sellform=sellform)
    

@app.route('/redeem_coupon', methods = ['POST','GET'])
@login_required
def redeem_coupon_page():
    couponform = RedeemCouponForm()
    if request.method == 'POST':
        temp_coupon = CouponData.query.filter_by(code = couponform.coupon_code.data).first()
        if temp_coupon:
            current_user.budget += temp_coupon.money
            db.session.delete(temp_coupon)
            db.session.commit()
            flash('Coupon redeemed successfully',category='success')
            return redirect(url_for('item_page'))
        else:
            flash('Unfortunately, coupon is expired or invalid', category='danger')
        
    return render_template('redeem_coupon.html',couponform=couponform)