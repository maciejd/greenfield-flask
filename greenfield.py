import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'greenfield.db'),
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    rv=sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initb_command():
    init_db()
    print 'Initialized the database.'

@app.route('/')
def show_suites():
    db = get_db()
    cur = db.execute('select id, title from test_suites order by id desc')
    suites = cur.fetchall()
    return render_template('show_suites.html', suites=suites)

@app.route('/runs')
def show_runs():
    db = get_db()
    cur = db.execute('select id, title, created from test_runs order by id desc')
    runs = cur.fetchall()
    return render_template('show_runs.html', runs=runs)

@app.route('/suite/<int:ts_id>')
def show_cases(ts_id):
    db = get_db()
    cur = db.execute('select id, title from test_cases where ts_id = ?', [ts_id])
    cases = cur.fetchall()
    return render_template('show_cases.html', cases=cases, ts_id=ts_id)

@app.route('/run/<int:run_id>')
def show_run(run_id):
    db = get_db()
    cur = db.execute('select e.id, c.title, e.status, e.updated from test_cases c join test_executions e on c.id = e.tc_id where e.tr_id = ?', [run_id])
    executions = cur.fetchall()
    return render_template('show_run.html', executions=executions)

@app.route('/add', methods=['POST'])
def add_suite():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into test_suites (title) values (?)', 
    [request.form['title']])
    db.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('show_suites'))

@app.route('/add_case', methods=['POST'])
def add_case():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into test_cases (title,ts_id) values (?,?)', 
    [request.form['title'], request.form['ts_id']])
    db.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('show_cases', ts_id=request.form['ts_id']))

@app.route('/add_run/<int:ts_id>', methods=['POST'])
def add_run(ts_id):
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur = db.execute('insert into test_runs (title) values (?)', [request.form['title']])
    db.commit()
    tr_id = cur.lastrowid
    cur = db.execute('select id from test_cases where ts_id = ?', [ts_id])
    case_ids = cur.fetchall()
    for tc_id in case_ids:
        db.execute('insert into test_executions (tc_id,tr_id,status) values (?,?,?)', 
    [tc_id[0], tr_id, 'UNEXECUTED'])
    db.commit()
    flash('New entry was succesfully posted')
    return redirect(url_for('show_runs'))

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
    db = get_db()
    db.execute('delete from test_suites where id = ?', [request.form['ts_id']])
    db.commit()
    flash('Test suite deleted')
    return redirect(url_for('show_suites'))

@app.route('/delete_case', methods=['POST'])
def delete_case():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from test_cases where id = ?', [request.form['tc_id']])
    db.commit()
    flash('Test case deleted')
    return redirect(url_for('show_cases', ts_id=request.form['ts_id']))

@app.route('/delete_run', methods=['POST'])
def delete_run():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('delete from test_runs where id = ?', [request.form['run_id']])
    db.commit()
    flash('Test run deleted')
    return redirect(url_for('show_runs'))
