from flask import Flask, request,render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_migrate import Migrate
import os

from flask_mysqldb import MySQL

#import flask-mysql
#from flaskext.mysql import MySQL

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db.name

app.config['MYSQL_HOST'] = 'zachgozlan.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'zachgozlan'
app.config['MYSQL_PASSWORD'] = 'iW_Dn6LzrqYu4Ap'
app.config['MYSQL_DB'] = 'zachgozlan$bids'

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#mysql = MySQL(app)

#flaskext.mysql version
#mysql = MySQL()
#app = mysql.init_app(app)

db_name = 'bids.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flask_app import routes, models, bid_calculation