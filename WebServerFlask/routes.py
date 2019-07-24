from flask import render_template, url_for, redirect, flash, request
from .forms import RegistationForm, LoginForm, PostForm
from .models import User
from WebServerFlask import app, bcrypt, db, r_client, REDIS_SET, REDIS_POST_TTL
from flask_login import login_user, current_user, logout_user, login_required
import datetime, time


#
# def home():
#     return render_template('home.html')

@app.route('/')
@app.route('/posts/', methods=['GET', 'POST'])
@login_required
def posts_page():
    dt = datetime.datetime.now()
    curr_time = time.mktime(dt.timetuple())
    r_client.zremrangebyscore(REDIS_SET, min='-inf', max=curr_time)
    if request.method == 'POST':
        r_client.zrem(REDIS_SET, request.values.get('post_name'))
        return redirect(url_for('posts_page'))
    redis_posts = r_client.zrange(REDIS_SET, 0, -1)
    return render_template('post.html', redis_posts=redis_posts)


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
        curr_time = time.mktime(dt.timetuple())
        r_client.zadd(REDIS_SET, {form.content.data: curr_time + REDIS_POST_TTL})
        flash('Post was created', 'success')
        return redirect(url_for('posts_page'))
    return render_template('new_post.html', form=form)
