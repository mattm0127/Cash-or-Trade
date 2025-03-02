from app import db
import datetime

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(40))
    date_joined = db.Column(db.DateTime, default=datetime.datetime.now())
    last_login = db.Column(db.DateTime, default=datetime.datetime.now())
    sales = db.Column(db.Integer)
    purchases = db.Column(db.Integer)

class Descriptions(db.Model):
    __tablename__ = 'descriptions'
    id = db.Column(db.Integer, primary_key=True)
    

class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.foreign_key(Users.id), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Integer, db.foreign_key(Descriptions.id), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tradeable = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='available')
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.now())


