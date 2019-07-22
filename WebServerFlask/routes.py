from flask import render_template, url_for, redirect, flash
from .forms import RegistationForm, LoginForm
from .models import Posts, User
from WebServerFlask import app, bcrypt, db


@app.route('/')
def home():
    for post in Posts.query.all():
        print(post.content)
    return render_template('home.html')


@app.route('/posts/')
def posts_page():
    posts = [
        'test',
        'test2',
    ]
    return render_template('post.html', posts=posts)


@app.route('/register/', methods=['GET', 'POST'])
def register():
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
    form = LoginForm()

    if form.validate_on_submit():
        flash('You log in system', 'success')
        return redirect(url_for('posts_page'))
    # else:
    #     flash('Invalid data', 'danger')
    return render_template('login.html', form=form)
