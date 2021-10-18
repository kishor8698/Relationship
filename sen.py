
from enum import unique
from os import stat_result
from flask import Flask, render_template, redirect, request, session,make_response
#from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.sqlite3'
app.config["SESSION_PERMANENT"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

'''
class emp(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    #city = db.Column(db.String(50))
    address= db.Column(db.String(100))
    state=db.Column(db.String(40))

class emp(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    address= db.Column(db.String(100))
'''    
class emp(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    address= db.Column(db.String(100))
    state= db.Column(db.String(100))
    pin_code= db.Column(db.String(100))
    
class Customer(db.Model):
    '''Customer table'''

    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(25))
    customer_email = db.Column(db.String(100), nullable=True)
    order_id = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer: {self.id} {self.customer_name}>'


class Order(db.Model):
    '''Order table'''
    
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.now)
    # Use datetime to generate a random 6 digit number from milliseconds.
    order_number = db.Column(db.Integer, default=datetime.now().strftime("%f"))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    
    def __repr__(self):
        return f'<OrderID: {self.id}>'
    
# result = emp.query.filter_by(name='kishor').first()
# db.session.delete(result)
# db.session.commit()
# result=emp(name='kishor',city='parola',address='maharashtra')
# db.session.add(result)
# db.session.commit()


@app.route("/")
def index():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")

    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
      # if form is submited
      
    if request.method == "POST":
        # record the user name
        session["name"] = request.form.get("name")
        
        # redirect to the main page
        return redirect("/")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
    

