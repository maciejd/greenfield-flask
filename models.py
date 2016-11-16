from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class TestCase(db.Model):
    __tablename__ = 'test_cases'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    ts_id = db.Column(db.Integer, db.ForeignKey('test_suites.id'))
    suite = db.relationship('TestSuite', backref=db.backref('cases', lazy='dynamic'))    

    def __init__(self, title, suite):
        self.title = title
        self.suite = suite

    def __repr__(self):
        return '<Test case %r>' % self.title

class TestSuite(db.Model):
    __tablename__ = 'test_suites'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Test suite %r>' % self.title

   
class TestRun(db.Model):
    __tablename__='test_runs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow())   

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Test run %r>' % self.title

class TestExecution(db.Model):
    __tablename__='test_executions'
    id = db.Column(db.Integer, primary_key=True)
    tc_id = db.Column(db.Integer, db.ForeignKey('test_cases.id'))
    tr_id = db.Column(db.Integer, db.ForeignKey('test_runs.id'))  
    testrun = db.relationship('TestRun', backref=db.backref('executions', lazy='dynamic'))
    testcase = db.relationship('TestCase', backref=db.backref('executions', lazy='dynamic'))  
    status = db.Column(db.String)
    updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, status, testcase, testrun):
        self.status = status
        self.testcase = testcase
        self.testrun = testrun

    def __repr__(self):
        return '<Test run %s %d %d>' % (self.status, self.tc_id, self.tr_id)

