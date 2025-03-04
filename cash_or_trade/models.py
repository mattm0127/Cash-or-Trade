from cash_or_trade.extensions import database as db
import datetime

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(40))
    date_joined = db.Column(db.DateTime, default=datetime.datetime.now())
    last_login = db.Column(db.DateTime, default=datetime.datetime.now())
    sales_amt = db.Column(db.Integer)
    purchases_amt = db.Column(db.Integer)

    items = db.relationship('Items', back_populates='users', cascade="all, delete")
    sales = db.relationship('Purchases', foreign_keys="Purchases.seller_id", back_populates='seller')
    bought = db.relationship('Purchases', foreign_keys="Purchases.buyer_id", back_populates='buyer')

class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete="CASCADE"), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description_id = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    tradeable = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='available')
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.now())

    users = db.relationship('Users', back_populates="items")
    descriptions = db.relationship('Descriptions', back_populates='items', cascade='all, delete')

class Descriptions(db.Model):
    __tablename__ = 'descriptions'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey(Items.id, ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    descr = db.Column(db.Text)
    img1 = db.Column(db.String(2048))
    img2 = db.Column(db.String(2048))
    img3 = db.Column(db.String(2048))
    img4 = db.Column(db.String(2048))
    img5 = db.Column(db.String(2048))

    items = db.relationship('Items', back_populates='descriptions')

class Purchases(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey(Items.id, ondelete="SET NULL"))
    seller_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete="SET NULL"))
    buyer_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete="SET NULL"))
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    seller = db.relationship('Users', foreign_keys=[seller_id], back_populates='sales')
    buyer = db.relationship('Users', foreign_keys=[buyer_id], back_populates='bought')
