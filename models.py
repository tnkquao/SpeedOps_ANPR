from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_table import Table, Col, LinkCol

app = Flask(__name__)
app.secret_key='HelloNoSpeedingHere'   # secret key used for encrypt and decrypt server data

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/speedops'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

engine = create_engine('mysql://root:@localhost/speedops', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

class admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    
    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=password


class owners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    home_address = db.Column(db.String(60))
    license_plate = db.Column(db.String(100))
    contact_1 = db.Column(db.Integer)
    contact_2 = db.Column(db.String(100))


class speeders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(100))
    name = db.Column(db.String(100))
    speed = db.Column(db.Integer)
    amount_fined= db.Column(db.Float(6, False, 2))
    location = db.Column(db.String(60))
    record_date = db.Column(db.DateTime, default=datetime.utcnow)
    #fine_paid = db.Column(db.Boolean, default=False)

'''
    def __init__(self, name, license_plate, speed, fine, location):
        self.name=name
        self.license_plate=license_plate
        self.speed=speed
        self.amount_fined = fine
        self.location = location
'''  

class log_track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, ):
        self.name=name



class Results(Table):
    classes = ['table', 'table-responsive', 'table-striped']

    id = Col('id', show=False)
    name = Col('Name')
    license_plate = Col('License_Plate')
    speed = Col('Speed')
    amount_fined = Col('Fine')
    location = Col('Location')
    record_date = Col('Date_Recorded')
    #edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    #delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)