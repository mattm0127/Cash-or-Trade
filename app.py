import os
import sqlite3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from cash_or_trade.blueprints import accounts, listings, purchases
from decouple import config

app = Flask(__name__)
# For Testing
# BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = 'sqlite:///' + os.path.join(BASE_PATH + '/app.db')
# print(DB_PATH)
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH

# For Production
app.config['SQLALCHEMY_DATABASE_URI'] = config("DATABASE_CONNECTION")

app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        from cash_or_trade import models
        db.create_all()
    app.run(debug=True)
