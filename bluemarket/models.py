from bluemarket import db
from bluemarket import bcrypt
from bluemarket import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length=30), unique = True , nullable = False)
    email_address = db.Column(db.String(length = 50), unique=True , nullable = False)
    password_hash = db.Column(db.String(length = 60), nullable = False)
    budget = db.Column(db.Integer() , nullable = False , default = 1000)
    items = db.relationship('Item' , backref = 'owned_user' , lazy = True)

    

    # this is like a security not able to change or manipulate the password
    @property
    def password(self):
        return self.password
    

    # password can be changed as hash by setting setter. It gets sets automatically when value is assigned
    @password.setter
    def password (self , plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
          
    def buy_check(self , item):
        if self.budget < item.price:
            return False
        else:
            return True


    def __repr__(self):
        return f'User -> {self.username}'


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    onwer = db.Column (db.Integer() , db.ForeignKey('user.id'))

    
    def __repr__(self):
        return f"Item {self.name}"
    
    
class CouponData(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    code = db.Column(db.String(length = 10),nullable = False)
    money = db.Column(db.Integer(),nullable=True)

