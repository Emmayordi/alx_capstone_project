# routes.py
from flask import render_template, redirect, url_for, flash, request,abort
from flask_login import login_required, current_user
from StayFitBlog import app, bcrypt,db
from StayFitBlog.models import User, Post,add_user
from StayFitBlog.forms import LoginForm, Register
from StayFitBlog.forms import AddPostForm
from flask_login import login_user,logout_user


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
            
            flash('Email address already registered.', 'danger')
            return render_template('register.html', title='Register', form=form)
        
    
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = User.query.filter_by(email=form.email.data).first()
        
        if result and bcrypt.check_password_hash(result.password_hash, form.password.data):
            login_user(result)
            flash('Login Successful', 'success')
            return redirect(url_for('posts'))  # Assuming you want to redirect to the homepage
    # Render the login template if not a POST request or if validation/login fails
    return render_template('login.html', title='Login', form=form)





@app.route('/posts')
@login_required
def posts():
    all_posts = Post.query.all()
    return render_template('posts.html', title='All Posts', posts=all_posts)

#Edite post
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # Forbidden access
    form = AddPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('edit_post.html', title='Edit Post', form=form, post=post)






#Add Post
@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts'))
    return render_template('add_post.html', title='Add Post', form=form)
#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return redirect(url_for('posts'))
    return render_template('post_detail.html', title=post.title, post=post)

