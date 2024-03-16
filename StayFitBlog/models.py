#models.py
from flask_login import UserMixin
from StayFitBlog import db, bcrypt ,login_manager 
from flask_bcrypt import generate_password_hash, check_password_hash  
import datetime

@login_manager.user_loader
def load_user(user_id):
   
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(1500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Get(title: {self.title}, author: {self.author.name})'
    
def add_user(form):
   
    name = form.name.data
    email = form.email.data
    password = form.password.data  

  
    hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Instantiate User with the correct field names
    user = User(name=name, email=email, password_hash=hashed_pwd)
    
    db.session.add(user)
    db.session.commit()
