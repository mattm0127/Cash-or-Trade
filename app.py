import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from cash_or_trade import views
from cash_or_trade.blueprints import accounts, listings, purchases

app = Flask(__name__)
BASE_PATH = os.path.abspath(os.path.dirname(__name__))
DB_PATH = 'sqlite:///' + os.path.join(BASE_PATH + 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
db = SQLAlchemy(app)