from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy()
bcrypt = Bcrypt(app)


from client_app.views import index
