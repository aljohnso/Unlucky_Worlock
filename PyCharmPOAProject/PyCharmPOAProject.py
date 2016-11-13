import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from DataBase.DataBaseControls.FlaskDatabaseMangment import init_db, get_db,connect_db,show_entries  #this should import the FlaskDatabaseMangment.py file Note you will need to change this if there is ever a change in file stucture

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path + "//DataBase", 'POA.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('PyCharmPOAProject_SETTINGS', silent=True)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print ('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
