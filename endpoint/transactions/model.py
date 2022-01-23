from app import db , ma
from enum import Enum
import datetime

# category enum
class Category(Enum):
    FOOD = 'food'
    ENTERTAINMENT = 'entertainment'
    TRANSPORT = 'transport'
    HEALTH = 'health'
    SAVINGS = 'savings'
    EDUCATION = 'education'
    FRIENDS_AND_FAMILY = 'friends_and_family'
    OTHER = 'other'


# Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    category = db.Column(db.Enum(Category))
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    description = db.Column(db.String(100))
    merchant = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, amount, category, date, description, merchant, user_id):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.merchant = merchant
        self.user_id = user_id


# Schema
class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'amount', 'category', 'date', 'description', 'merchant', 'user_id')


# Init schema
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)