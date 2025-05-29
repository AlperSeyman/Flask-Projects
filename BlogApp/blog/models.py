from blog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False)
    email = db.Column(db.String(length=120), unique=True, nullable=False) 
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f"User Name: {self.username} Email: {self.email} Image File: {self.image_file}"
    

    def get_reset_token(self):
        s = Serializer(app.config["SECRET_KEY"])
        token = s.dumps({'user_id': self.id})
        return token
    
    @staticmethod
    def verify_reset_token(token, expire_sec=180):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, max_age=expire_sec)["user_id"]
        except:
            return None
        
        return User.query.get(user_id)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Title: {self.title} Date Posted: {self.date_posted}"