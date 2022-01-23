from app import db , ma
# import transaction model
from endpoint.transactions.model import Transaction


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    admin = db.Column(db.Boolean)



    def __init__(self, public_id, name, email, password, admin):
        self.public_id = public_id
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin


# user Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'admin')


# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)