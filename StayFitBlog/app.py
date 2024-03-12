from flask_migrate import Migrate
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from forms import Register, AddPostForm
from models import db, Post, User, add_post_to_db, add_user  # Import all models

import datetime
from config import ConfigClass

app = Flask(__name__)
app.config.from_object(ConfigClass)
csrf = CSRFProtect(app)
db.init_app(app)  # Initialize db with the app
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

#  (rest of routes)


# Define routes here
@app.route('/')
def home():
    return render_template('home.html', title='Homepage', current_year=datetime.datetime.now().year)

# New route for about page
@app.route('/about')
def about():
    return render_template('about.html', title='About')
# ... (other routes)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = Register()
    if form.validate_on_submit():
        add_user(form)
        flash('Registeration is successull!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form, current_year=datetime.datetime.now().year)


# ... (other routes)


@app.route('/posts')
def posts():
    
    all_posts = Post.query.all()
    return render_template('posts.html', title='All Posts', posts=all_posts, current_year=datetime.datetime.now().year)

# ... (other routes)

@app.route('/add_post', methods=('GET', 'POST'))
def add_post():
  
    form = AddPostForm()
    if form.validate_on_submit():
        # Add logic to save the post to the database
        add_post_to_db(form)
        return redirect(url_for('posts'))

    return render_template('add_post.html', title='Add Post', form=form, current_year=datetime.datetime.now().year)
# New route for about page

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
