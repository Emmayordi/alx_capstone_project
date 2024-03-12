# models.py
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    # Let SQLAlchemy generate the backref for posts
    posts = db.relationship('Post', lazy=True)

    def __repr__(self):
        return f'name: {self.name}, email: {self.email}'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(1500), nullable=False)
    date = db.Column(db.String(120), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Let SQLAlchemy generate the backref for the User relationship
    user = db.relationship('User', lazy=True)

    def __repr__(self):
        return f'title: {self.title}, author: {self.user.name}'
    
def add_user(form):
    name = form.name.data
    email = form.email.data
    password = form.password.data
    hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = User(name=name, email=email, password=hashed_pwd)
    db.session.add(new_user)
    db.session.commit()


def add_post_to_db(form):
    title = form.title.data
    content = form.content.data
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Assuming you have a current_user object representing the logged-in user
    user_id = current_user.id  # Make sure to import current_user from flask_login

    new_post = Post(title=title, content=content, date=date, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
