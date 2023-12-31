from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import Length  , EqualTo , Email , DataRequired , ValidationError
from bluemarket.models import User

class RegisterForm(FlaskForm):

# so this flask form has a feature it finds the function starting with validate
# and _fieldentry and it checks for validation

# why username.data ?? becoz username_to_check is a object but we need to compare the username itself
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username Already Exists!!")
        
    def validate_email_address(self,email_address_to_check):
        email = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email:
            raise ValidationError("Email Address Already Exists !! ")    


# these are the ways to create the forms 
# any no of validators can be added in the list
    username = StringField(label = 'User Name:' , validators=[Length(min=4,max=30) , DataRequired()])
    email_address = StringField(label='Email Address:' , validators=[Email() , DataRequired()])
    password1 = PasswordField(label = 'Password:' , validators=[Length(min=6) , DataRequired()])
    password2 = PasswordField(label = 'Confirm Password:', validators=[EqualTo('password1') , DataRequired()])
    submit = SubmitField(label = 'Create Account')


class LoginForm(FlaskForm):
    username = StringField(label = 'User Name: ',validators=[DataRequired()])
    password = PasswordField(label = 'Password: ',validators=[DataRequired()])
    submit = SubmitField(label = 'Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label= 'Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label= 'Sell Item!') 

class RedeemCouponForm(FlaskForm):
    coupon_code = PasswordField(label='Coupon Code: ')
    submit = SubmitField(label = 'Redeem')       

class AddItem(FlaskForm):
    itemname = StringField(label='Name: ')
    itemprice = StringField(label ='Price: ')
    submit = SubmitField(label = 'Add Item')     

class GenerateCoupon(FlaskForm):    
    submit = SubmitField(label= 'Generate Coupon !!') 