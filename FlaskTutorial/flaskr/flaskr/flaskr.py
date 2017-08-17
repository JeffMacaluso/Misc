import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# Create the actual application instance and initializes with the
# config from the same file in flaskr.py
app = Flask(__name__)  # Create the application instance
app.config.from_object(__name__)  # Load config from this file, flaskr.py

# Database Path
# Load default config and override config from an environment variable
# Works similarly to a dict, and updating with new values
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',  # Keeps client side secure
    USERNAME='admin',
    PASSWORD='default'
))

# Enable robust configuration setups
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """
    Connects to the specific database

    Allows connection from either IPython or a script
    """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row  # Represents rows
    return rv


def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application conext.

    This is an application context
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """
    Closes the database again at the end of the request
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    """
    Initializes the database to the application
    """
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')  # Registers a new command with the flask script
def initdb_command():
    """
    Wrapper that initializes the database
    """
    init_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    """
    Shows all entries stored in the database.  Listens on the root of the
    application and will select title and text from the database.  The one
    with the highest id (newest entry) will beo n top.
    """
    db = get_db()  # Connects to the database
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    """
    Allows the user to add new entries if they're logged in.  Only responds
    to POST requests.
    """
    # Ensure the user is logged in
    if not session.get('logged_in'):
        abort(401)
    db = get_db()  # Connects to the database
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Signs the user in.  Checks the username and password against those in the
    configuration and sets logged_in key for the session.
    """
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """
    Removes the user key from the session
    """
    session.pop('logged_in', None)  # Pop deletes key if exists, else nothing
    flash('You were logged out')
    return redirect(url_for('show_entries'))    