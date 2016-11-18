from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
import datetime
from database import Base

class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    ts_id = Column(Integer, ForeignKey('test_suites.id'))
    suite = relationship('TestSuite', backref=backref('cases', lazy='dynamic', cascade="all, delete-orphan"))    

    def __init__(self, title, suite):
        self.title = title
        self.suite = suite

    def __repr__(self):
        return '<Test case %r>' % self.title

class TestSuite(Base):
    __tablename__ = 'test_suites'
    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Test suite %r>' % self.title

   
class TestRun(Base):
    __tablename__='test_runs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)   

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Test run %r>' % self.title

class TestExecution(Base):
    __tablename__='test_executions'
    id = Column(Integer, primary_key=True)
    tc_id = Column(Integer, ForeignKey('test_cases.id'))
    tr_id = Column(Integer, ForeignKey('test_runs.id'))  
    testrun = relationship('TestRun', backref=backref('executions', lazy='dynamic', cascade="all, delete-orphan"))
    testcase = relationship('TestCase', backref=backref('executions', lazy='dynamic'))  
    status = Column(String)
    updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, status, testcase, testrun):
        self.status = status
        self.testcase = testcase
        self.testrun = testrun

    def __repr__(self):
        return '<Test run %s %d %d>' % (self.status, self.tc_id, self.tr_id)

