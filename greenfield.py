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

@app.route('/suite/<int:ts_id>')
def show_cases(ts_id):
    db = get_db()
    cur = db.execute('select id, title from test_cases where ts_id = ?', [ts_id])
    cases = cur.fetchall()
    return render_template('show_cases.html', cases=cases, ts_id=ts_id)

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
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

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
