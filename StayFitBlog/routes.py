from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from StayFitBlog import app, bcrypt, db
from StayFitBlog.models import User, Post, Comment,add_user
from StayFitBlog.forms import LoginForm, RegisterForm, AddPostForm, CommentForm

from bleach import clean

@app.route('/search')
def search():
    query = request.args.get('q', '')  # Getting the search term from the query string
    # Perform search logic here, possibly querying your database
    # For demonstration purposes, we'll just return a simple response
    return f"Search results for: {query}"

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
#Login
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

#Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        add_user(form)  
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)

#Logoout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
#Add_Post
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
#Post deatal
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)  # Retrieve the post or 404
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # Create and add the new comment to the database
            comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been added.', 'success')
        else:
            flash('You need to be logged in to comment.', 'danger')
        return redirect(url_for('post_detail', post_id=post_id))
    
    comments = Comment.query.filter_by(post_id=post_id).all()  # Retrieve all comments for this post
    return render_template('post_detail.html', post=post, form=form, comments=comments)


#Commint
@app.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
    else:
        for error in form.content.errors:
            flash(error, 'danger')
    return redirect(url_for('post_detail', post_id=post_id))
#Edit
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.author.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit_post.html', title='Edit Post', form=form, post=post)