from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

POSTGRES_URL = "127.0.0.1"
POSTGRES_USER = "Dinar5"
POSTGRES_PW = ""
POSTGRES_DB = "flaskdb"
app.config['SECRET_KEY'] = 'b1af4eff3b8bde7a0982fcbc9905fb82'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2' \
                                        '://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                                           pw=POSTGRES_PW,
                                                                           url=POSTGRES_URL,
                                                                           db=POSTGRES_DB)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from WebServerFlask import routes
