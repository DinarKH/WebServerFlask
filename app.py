from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES_URL = "127.0.0.1"
POSTGRES_USER = "Dinar5"
POSTGRES_PW = ""
POSTGRES_DB = "flaskdb"

app.config['SECRET_KEY'] = 'b1af4eff3b8bde7a0982fcbc9905fb82'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                                                              pw=POSTGRES_PW,
                                                                                              url=POSTGRES_URL,
                                                                                              db=POSTGRES_DB)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return self.username


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


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
