# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# import hashing function and hashed password comparison function
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from werkzeug import security

# create the Flask app
from flask import Flask, render_template, request, jsonify, flash
app = Flask(__name__)

from flask import request
app.secret_key="123"
#importing session from flask
from flask import session, redirect

#Flask_Login
from flask_login import login_user, current_user
from flask_login import LoginManager
from flask_login import logout_user
from flask_login import login_required

#preventing XSS attacks
from markupsafe import escape

#intialising login LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view="login"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

# select the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set up a 'model' for the data you want to store
from db_schema import db, User, Reciept, Bill, dbFiller

# init the database so it can connect with our app
db.init_app(app)

# change this to False to avoid resetting the database every time this app is restarted
resetdb = True
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        userItems=dbFiller()


#route to the index
@app.route('/')
def index():
    users=User.query.all()
    reciepts = Reciept.query.all()
    bills = Bill.query.all()
    return render_template('index.html')


@app.route('/html/register.html', methods=['GET', 'POST'])
def register():
    errorMessage=""
    if request.method == 'POST':
        check=True;
        username = escape(request.form['username'])
        userPassword = security.generate_password_hash(escape(request.form['password']), "sha256")
        userPasswordCheck = escape(request.form['passwordCheck'])
        userEmail = escape(request.form['email'])
        #Checking if any inputs were empty
        if(username==""or userPassword=="" or userPasswordCheck=="" or userEmail==""):
            errorMessage+="Please fill in all the fields"
            check=False
        #Checking if an existing user has this username
        userExists=User.query.filter_by(username=username).all()
        #Checking if an existing user has this email
        emailExists=User.query.filter_by(email=userEmail).all()
        #Checking if the user password is the same as the password they retyped
        if(security.check_password_hash(userPassword,userPasswordCheck))==False:
            errorMessage+=" The passwords did not match"
            check=False
        if len(userExists)!=0:
            errorMessage+=" An existing user has this name"
            check=False
        if len(emailExists)!=0:
            errorMessage+=" An existing user has this email"
            check=False
        if(check):
            db.session.add(User(username,userPassword,userEmail))
            db.session.commit()
            user=User.query.filter_by(username=username).first()
            login_user(user)
            return redirect('/html/bills.html')
    return render_template('/html/register.html',errorMessage=errorMessage)



@app.route('/html/login.html', methods=['GET', 'POST'])
def login():
    #Only running code if a POST request is sent
    if request.method == 'POST':
        username = escape(request.form['username'])
        userPassword=escape(request.form['userPassword'])
        validUser=User.query.filter_by(username=username).first()
        if(validUser is not None):
            savedPassword=validUser.password
            if(security.check_password_hash(savedPassword,userPassword)):
                login_user(validUser)
                return redirect('/html/bills.html')
    #Displaying the login page if the user input incorrect details
    return render_template('/html/login.html')



@app.route('/html/bills.html', methods=['GET','POST'])
@login_required
def billPage():
    if request.method == 'POST':
        return addBill()
    allBills=Bill.query.filter_by().all();
    allUsers=User.query.filter_by().all();
    allUserNames=[]
    length=0
    for user in allUsers:
        allUserNames.append(user.username)
        length=length+1
    return render_template('/html/bills.html',allBills=allBills, allUserNames=allUserNames, length=length)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('/index.html')


@app.route('/html/addBill', methods=['POST'])
@login_required
def addBill():
    #intialising variables
    billDetails={}
    allUsers=User.query.filter_by().all();
    billName=escape(request.form['billName'])
    length=escape(request.form['length'])
    length=int(length)
    value=escape(request.form['totalValue'])
    #Adding entries to reciept
    for count in range(length):
        key="c"+str(count)
        index=int(escape(request.form[key]))
        username=allUsers[index].username
        amountToPay=escape(request.form[str(index)])
        billDetails[str(count)]=username+" owes £"+str(amountToPay)
        db.session.add(Reciept(username,amountToPay,billName))
    db.session.add(Bill(billName,value))
    db.session.commit()
    billDetails['billName']=billName
    return jsonify(billDetails)



@app.route('/html/displayBill', methods=['POST'])
@login_required
def billDisplay():
    billName=escape(request.form['billName'])
    billDetails=Reciept.query.filter_by(billName=billName).all()
    returnDetails={}
    for index in range(len(billDetails)):
        #Adding the usernames to returnDetails
        key="username"+str(index)
        value=billDetails[index].userName
        returnDetails[key]=value

        key="amountPaid"+str(index)
        value=billDetails[index].amountPaid
        returnDetails[key]=value

        key="amountDue"+str(index)
        value=billDetails[index].amountDue
        returnDetails[key]=value
    returnDetails["length"]=len(billDetails)
    returnDetails["billName"]=billName
    return jsonify(returnDetails)

@app.route('/html/payBill', methods=['POST'])
@login_required
def payBill():
    username=current_user.username
    billName=escape(request.form["billName"])
    amountPaid=escape(request.form["amountPaid"])
    reciept=Reciept.query.filter_by(userName=username, billName=billName).first()
    newAmountPaid=int(reciept.amountPaid)+int(amountPaid)
    reciept.amountPaid=newAmountPaid
    db.session.commit()
    recieptData={}
    #Checking if everyone has paid the amount due for the bill
    allBillReciepts=Reciept.query.filter_by(billName=billName).all()
    isPaid=True
    for item in allBillReciepts:
        if(item.amountDue>item.amountPaid):
            isPaid=False
    if isPaid:
        bill=Bill.query.filter_by(billName=billName).first()
        bill.status="PAID"
        recieptData["status"]="PAID"
    else:
        recieptData["status"]="PENDING"
    db.session.commit()
    recieptData["amountPaid"]=reciept.amountPaid
    recieptData["amountDue"]=reciept.amountDue
    recieptData["username"]=reciept.userName
    recieptData["billName"]=reciept.billName
    return jsonify(recieptData)


@app.route('/html/getBillData', methods=['GET'])
def retrieveData():
    data={}
    bills=Bill.query.filter_by().all()
    i=0
    for bill in bills:
        data["billname"+str(i)]=bill.billName
        i=i+1
    data['length']=i
    return jsonify(data)
