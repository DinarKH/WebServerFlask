from flask import render_template, url_for, redirect, flash, request
from .forms import RegistationForm, LoginForm, PostForm
from .models import Posts, User
from WebServerFlask import app, bcrypt, db, r_client
from flask_login import login_user, current_user, logout_user, login_required
import datetime, time


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/posts/', methods=['GET', 'POST'])
@login_required
def posts_page():
    dt = datetime.datetime.now()
    s = time.mktime(dt.timetuple())
    print('Current time is {}'.format(s))
    r_client.zremrangebyscore('post_set', min='-inf', max=s)
    if request.method == 'POST':
        r_client.zrem('post_set', request.values.get('post_name'))
        return redirect(url_for('posts_page'))
    redis_posts = r_client.zrange('post_set', 0, -1)
    posts = Posts.query.all()
    return render_template('post.html', posts=posts, redis_posts=redis_posts)


@app.route('/post/<int:post_id>/delete/', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post was deleted')
    return redirect(url_for('posts_page'))


@app.route('/register/', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account create', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # flash('You log in system', 'success')
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid data', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('posts_page'))


@app.route('/post/new/', methods=['GET', 'POST'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        dt = datetime.datetime.now()
        s = time.mktime(dt.timetuple())
        print('Current time is {}'.format(s))
        r_client.zadd('post_set', {form.content.data: s + 50})
        # print(r_server.zremrangebyscore('post_set', min='-inf', max=s))
        # print(r_client.zrange('post_set', 0, -1, withscores=True))
        # post = Posts(title=form.title.data, content=form.content.data)
        # db.session.add(post)
        # db.session.commit()
        # flash('Post was created', 'success')
        return redirect(url_for('posts_page'))
    return render_template('new_post.html', form=form)
