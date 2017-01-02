import os
import sqlite3
from Forms.POAForms import MakeTripFormPOA, AddToTripPOA
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from DatabaseConnection.DatabaseConnection import DatabaseConnection
from flask_bootstrap import Bootstrap

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


@app.route('/', methods=['GET', 'POST'])
def Main():
    db = get_db()
    entries = db.checkTrip()
    entriesClean = []
    for a in entries:
        b = [list(map(lambda x: str(x), a))]
        entriesClean += b
    return render_template("HomePage.html", entries=entriesClean)


@app.route("/trips/<TripKey>")
def TripPage(TripKey):
    """
    :param TripKey: The name of the trip
    :return: renders template of the selected trip with detailed information
    """
    db = get_db()
    tripDetails, meta, ParticpantInfo = db.getTrip(TripKey)
    print(tripDetails)
    print(meta)
    print(ParticpantInfo)
    return render_template("TripPage.html", Tripinfo=tripDetails[0], TripMeta=meta[0], ParticpantInfo= ParticpantInfo)


@app.route('/addTrip', methods=['POST','GET'])
def add_Trip():
    db = get_db()
    form = MakeTripFormPOA()
    if request.method == 'POST':
        # print(form.data)  # returns a dictonary with keys that are the feilds in the table
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('CreateTrip.html', form=form)
        else:
            db.AddTrip(form.data)
            flash('New entry was successfully posted')
            return redirect(url_for('Main'))
    elif request.method == 'GET':
        return render_template('CreateTrip.html', form=form)


@app.route('/addParticipant/<FormKey>',  methods=['POST','GET'])
def add_Participant(FormKey):
    db = get_db()
    tripname = db.cursor.execute('select Trip_Name, Participant_num, Partcipant_cap from'
                                 ' Master WHERE id =' + str(FormKey)).fetchall()
    form = AddToTripPOA()
    if request.method == 'GET':
        return render_template('Add_Particpant.html', form=form, tripname=tripname)
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('Add_Particpant.html', form=form, tripname=tripname)
        else:
            db.Addparticipant(form.data, str(FormKey))
            flash('New entry was successfully posted')
            return redirect(url_for('TripPage', TripKey=str(FormKey)))


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.closeConnection()


# Calls connect DB
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = DatabaseConnection(app.config['DATABASE'])
    return g.sqlite_db


def init_db():
    """
    will go to the schema flile
    :return: VOID
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('ApplicationDataManger.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == '__main__':
    Bootstrap(app)
    app.run()
    app.run(debug=True)
