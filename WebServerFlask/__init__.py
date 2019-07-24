from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import redis

app = Flask(__name__)

POSTGRES_URL = "127.0.0.1"
POSTGRES_USER = "Dinar5"
POSTGRES_PW = ""
POSTGRES_DB = "flaskdb"
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_SET = 'post_set'
REDIS_POST_TTL = 400

app.config['SECRET_KEY'] = 'b1af4eff3b8bde7a0982fcbc9905fb82'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2' \
                                        '://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                                           pw=POSTGRES_PW,
                                                                           url=POSTGRES_URL,
                                                                           db=POSTGRES_DB)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
r_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

from WebServerFlask import routes
