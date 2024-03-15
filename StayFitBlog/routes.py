# routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from StayFitBlog import app, bcrypt,db
from StayFitBlog.models import User, Post,add_user
from StayFitBlog.forms import LoginForm, Register

from flask_login import login_user


@app.route('/')
def home():
    return render_template('home.html', title='Homepage')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            # If a user is found with the submitted email, flash a message and return to the form
            flash('Email address already registered.', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # Proceed with registration because the email is not in use
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Notify the user of successful registration
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    # For GET requests or if form validation fails, just render the registration form
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = User.query.filter_by(email=form.email.data).first()
        if result and bcrypt.check_password_hash(result.password, form.password.data):
            login_user(result)
            flash('Login Successful', 'success')
            return redirect(url_for('posts'))
    return render_template('login.html', title='Login', form=form)



@app.route('/posts')
@login_required
def posts():
    all_posts = Post.query.all()
    return render_template('posts.html', title='All Posts', posts=all_posts)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    """"
    form = AddPostForm()
    if form.validate_on_submit():
        # Corrected line to use 'user_id' instead of 'author_id'
        new_post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts'))
    """
    return render_template('add_post.html', title='Add post')
