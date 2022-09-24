from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

#importing UserMixin
from flask_login import UserMixin
# create the database interface
db = SQLAlchemy()

# a model of a user for the database
class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(50), unique=True)

    def __init__(self, username, password, email):
        self.username=username
        self.password=password
        self.email=email


# a model of Reciept for the database
# it refers to a user and how much they need to pay towards a specific bill
#Each user can have multiple Reciepts and each reciepts
class Reciept(db.Model):
    __tablename__='reciepts'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.Text(), db.ForeignKey("users.username"))# this is a foreign key to link to the Users table
    amountDue = db.Column(db.Integer)
    amountPaid = db.Column(db.Integer)
    billName = db.Column(db.Text(), db.ForeignKey("bills.billName"))  # this is a foreign key to link to the bills table

    def __init__(self, username, amountDue,billName):
        self.userName=username
        self.amountDue = amountDue
        self.amountPaid = 0
        self.billName = billName


# a model of a Bill  for the database
# it refers to a bill
#Each bill has multiple Reciepts
class Bill(db.Model):
    __tablename__='bills'
    billName = db.Column(db.Text(), primary_key=True)
    totalAmount = db.Column(db.Integer)
    status = db.Column(db.Text())



    def __init__(self, billName, totalAmount):
        self.billName=billName
        self.totalAmount=totalAmount
        self.status="PENDING"


def dbFiller():
    1==1
