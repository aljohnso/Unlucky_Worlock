import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
# from DataBase.DataBaseControls.FlaskDatabaseMangment import init_db,show_entries  #this should import the FlaskDatabaseMangment.py file Note you will need to change this if there is ever a change in file stucture

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'POA.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('PYCHARMPOAPROJECT_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select Trip_Name, Trip_Capacity, Trip_Info, Trip_Participants from  Trips order by id desc')
    entries = cur.fetchall()
    return render_template("POACreateTrip.html", entries=entries)


@app.route("/trips/<TripKey>")
def show_trip(TripKey):
    """
    :param TripKey: The name of the trip
    :return: renders template of the selected trip with detailed information
    """
    db = get_db()
    DBComand = 'select Trip_Name, Trip_Capacity, Trip_Info, Trip_Participants from Trips WHERE id=' + TripKey
    #DBComand constructs the SQLite3 request for the DB
    cur = db.execute(DBComand)
    tripDetails = cur.fetchall()
    return render_template("TripPage.html", info=tripDetails[0])


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
    db = get_db()
    info = [request.form['TripName'], request.form['CarCap'], request.form['TripDescription'], request.form["LeaderName"]]
    print(info)
    db.execute('insert into Trips (Trip_Name,Trip_Capacity, Trip_Info, Trip_Participants ) values (?, ?, ?, ?)',info)#Fairly obvious but make sure that the ? marks are the same as the number feilds
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

#*****************************************************************
#*****************************************************************
#Database Functions that are here temp will be moved to FlaskDatabase Mangment in the future
#*****************************************************************
#*****************************************************************
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# Calls connect DB
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    """
    will go to the schema flile
    :return: VOID
    """
    # db = get_db()
    # with app.open_resource('schema.sql', mode='r') as f:
    #     db.cursor().executescript(f.read())
    # db.commit()
    with app.app_context():
        db = get_db()
        with app.open_resource('ApplicationDataManger.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def show_entries(SQL):
    """
    Example show_entries('select title, text from entries order by id desc')
    :param SQL: SQL code that will call table info to be returned
    :return: entries form sql table look up
    """
    db = get_db()
    cur = db.execute(SQL)
    entries = cur.fetchall()
    return entries

if __name__ == '__main__':
    app.run()
    app.debug = True