import bcrypt
from cash_or_trade.extensions import db
from cash_or_trade.models import Users, Items, Descriptions, Purchases

class DBClient:
    def __init__(self):
        None