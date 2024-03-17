from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from StayFitBlog import app, bcrypt, db
from StayFitBlog.models import User, Post, Comment,add_user
from StayFitBlog.forms import LoginForm, RegisterForm, AddPostForm, CommentForm

from bleach import clean

@app.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm()
    if login_form.validate_on_submit() and request.method == 'POST' and not current_user.is_authenticated:
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, login_form.password.data):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    posts = Post.query.all()
    return render_template('home.html', posts=posts, login_form=login_form if not current_user.is_authenticated else None)
#Healthy Life Style
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect to home if already logged in
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Assuming email is used for login
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)  # Assuming you have a 'remember' field in your LoginForm
            next_page = request.args.get('next')  # Redirect to the next page if it exists and is safe
            
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('home')
                
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


from flask import flash


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        add_user(form)  
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('add_post.html', title='Add Post', form=form)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        safe_content = clean(form.content.data)
        comment = Comment(content=safe_content, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
    elif form.validate_on_submit() and not current_user.is_authenticated:
        flash('You need to login to comment.', 'info')
        return redirect(url_for('login', next=url_for('post_detail', post_id=post_id)))
    comments = Comment.query.filter_by(post_id=post_id).all()  # Assuming you have a way to retrieve comments
    return render_template('post_detail.html', title=post.title, post=post, form=form, comments=comments)
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.id != current_user.id:
        flash('You cannot edit this post.', 'danger')
        return redirect(url_for('home'))
    # Proceed with edit logic
