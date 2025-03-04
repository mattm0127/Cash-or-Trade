import os
import sqlite3

from flask import Flask, render_template, redirect, url_for
from cash_or_trade.extensions import database
from cash_or_trade.blueprints import accounts, items, listings, purchases
from decouple import config

app = Flask(__name__)
app.secret_key = config("SECRET_KEY")
enviornment = 'dev'
### If DATABASE_CONNECTION not in .env a sqlite3 db is started. ###
if config("DATABASE_CONNECTION", default=False):
    app.config['SQLALCHEMY_DATABASE_URI'] = config("DATABASE_CONNECTION")
    enviornment = 'production'
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = 'sqlite:///' + os.path.join(BASE_PATH + '/app.db')
    print(DB_PATH)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    enviornment = 'dev'

    ### For Production ###
# app.config['SQLALCHEMY_DATABASE_URI'] = config("DATABASE_CONNECTION")

app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
database.init_app(app)

app.register_blueprint(accounts.accounts)
app.register_blueprint(items.items)
app.register_blueprint(listings.listings)
app.register_blueprint(purchases.purchases)

@app.route('/')
def home():
    return redirect(url_for('listings.home'))

if __name__ == '__main__':
    with app.app_context():
        from cash_or_trade import models
        database.create_all()
       ### FOR TESTING ###
    if enviornment == 'production':
        app.run(host='0.0.0.0', debug=False)
    else:
        app.run(debug=True)
