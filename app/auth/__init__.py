from flask import Blueprint
from flask import Flask
import pymysql.cursors
from flask_sqlalchemy import SQLAlchemy
from .users import *

auth = Blueprint('auth', __name__)





# Initialize app from flask
app = Flask(__name__)

# Configure MySQL
config = pymysql.connect(host='192.168.64.2',
                         user='root',
                         password='',
                         db='NYUSHer',
                         charset='utf8',
                         cursorclass=pymysql.cursors.DictCursor)


if __name__ == "__main__":
	app.run('127.0.0.1', 5005, debug = True)
