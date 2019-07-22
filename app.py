from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistationForm, LoginForm
import sys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b1af4eff3b8bde7a0982fcbc9905fb82'


@app.route('/')
def home():
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
        return redirect(url_for('posts_page'))
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


if __name__ == '__main__':
    app.run(debug=True)
