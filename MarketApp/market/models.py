from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password
    
    
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, user_password):
        return bcrypt.check_password_hash(self.password_hash, user_password)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{self.budget:,}$"
        else:
            return f"{self.budget}$"
        
    def can_purchase(self, item):
        return self.budget >= item.price
    
    def can_sell(self, item):
        return item in self.items
    
    
    

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True) 
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'


    def buy_item(self, user):         
        self.owner_id = user.id
        user.budget -= self.price
        db.session.commit()

    def sell_item(self, user):
        self.owner_id = None
        user.budget += self.price
        db.session.commit()
