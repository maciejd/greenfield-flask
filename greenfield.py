import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
from database import db_session, engine
from models import TestSuite,TestCase,TestRun,TestExecution

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='development_key'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/suites')
def show_suites():
    suites = TestSuite.query.all()
    return render_template('show_suites.html', suites=suites)

@app.route('/')
def show_runs():
    runs = TestRun.query.all()
    suites = TestSuite.query.all()
    return render_template('show_runs.html', runs=runs, get_results=get_results, suites=suites)

@app.route('/suite/<int:ts_id>')
def show_cases(ts_id):
    suite = TestSuite.query.filter(TestSuite.id == ts_id).first()
    cases = suite.cases.all()
    return render_template('show_cases.html', cases=cases, suite=suite)

@app.route('/run/<int:run_id>')
def show_run(run_id):
    statuses = ['UNEXECUTED','PASSED','FAILED','BLOCKED']
    run = TestRun.query.filter(TestRun.id == run_id).first()
    executions = run.executions.all()
    return render_template('show_run.html', run=run, executions=executions, statuses=statuses)

@app.route('/executions/<int:case_id>')
def show_executions(case_id):
    executions = TestCase.query.filter(TestCase.id == case_id).first().executions.all()
    return render_template('show_executions.html', executions=executions)

@app.route('/add', methods=['POST'])
def add_suite():
    if not session.get('logged_in'):
        abort(401)
    ts = TestSuite(request.form['title'])
    db_session.add(ts)
    db_session.commit()
    ts_id = ts.id
    flash('New entry was succesfully posted')
    return redirect(url_for('show_cases', ts_id=ts_id))

@app.route('/add_case', methods=['POST'])
def add_case():
    if not session.get('logged_in'):
        abort(401)
    tc = TestCase(request.form['title'], TestSuite.query.filter(TestSuite.id == request.form['ts_id']).first())
    db_session.add(tc)
    db_session.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('show_cases', ts_id=request.form['ts_id']))

@app.route('/add_run', methods=['POST'])
def add_run():
    if not session.get('logged_in'):
        abort(401)
    ts_id = request.form['ts_id']
    cases = TestSuite.query.filter(TestSuite.id == ts_id).first().cases.all()
    if len(cases) == 0:
        flash('Add test case before creating test run')
        return redirect(url_for('show_cases', ts_id=ts_id))
    else:    
        run = TestRun(request.form['title'])
        db_session.add(run)
        db_session.commit()
        run_id = run.id
        for case in cases:
            e = TestExecution('UNEXECUTED', case, run)
            db_session.add(e)
            db_session.commit()
        flash('New entry was succesfully posted')
        return redirect(url_for('show_run', run_id=run_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid username'
        elif request.form['password'] != 'admin':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
    	    flash('You were logged in')
            return redirect(url_for('show_suites'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_suites'))

@app.route('/delete', methods=['POST'])
def delete_suite():
    if not session.get('logged_in'):
        abort(401)
    s = TestSuite.query.filter(TestSuite.id == request.form['ts_id']).first()
    db_session.delete(s)
    db_session.commit()
    flash('Test suite deleted')
    return redirect(url_for('show_suites'))

@app.route('/delete_case', methods=['POST'])
def delete_case():
    if not session.get('logged_in'):
        abort(401)
    c = TestCase.query.filter(TestCase.id == request.form['tc_id']).first()
    db_session.delete(c)
    db_session.commit()
    flash('Test case deleted')
    return redirect(url_for('show_cases', ts_id=request.form['ts_id']))

@app.route('/delete_run', methods=['POST'])
def delete_run():
    if not session.get('logged_in'):
        abort(401)
    r = TestRun.query.filter(TestRun.id == request.form['run_id']).first()
    db_session.delete(r)
    db_session.commit()
    flash('Test run deleted')
    return redirect(url_for('show_runs'))

@app.route('/update_result', methods=['POST'])
def update_result():
    if not session.get('logged_in'):
        abort(401)
    e = TestExecution.query.filter(TestExecution.id == request.form['ex_id']).first()
    e.status=request.form['status']
    db_session.commit()
    return redirect(url_for('show_run', run_id=request.form['run_id']))  

def get_results(tr_id):
    exs = TestRun.query.filter(TestRun.id == tr_id).first().executions.all()
    cur = engine.execute('select status, count(*) as result_count from test_executions where tr_id = ? group by status', [tr_id])
    results = cur.fetchall()
    total = 0
    for result in results:
        total+=result['result_count']
    d={}
    for result in results:
        d[result['status']]=round(result['result_count']/float(total)*100, 0)
    return d
