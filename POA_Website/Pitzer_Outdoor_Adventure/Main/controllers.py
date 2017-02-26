from Forms.POAForms import MakeTripFormPOA, AddToTripPOA
from flask import  request, redirect, url_for, \
     render_template, flash,Blueprint
from DatabaseConnection.Database import db
import json
import flask
import httplib2
import apiclient as google
from oauth2client import client
import os
main = Blueprint('main', __name__, template_folder='templates')


@main.route('/', methods=['GET', 'POST'])
def Main():
    entries = db.checkTrip()
    entriesClean = []
    for a in entries:
        b = [list(map(lambda x: str(x), a))]
        entriesClean += b
    return render_template("HomePage.html", entries=entriesClean)


@main.route("/trips/<TripKey>")
def TripPage(TripKey):
    """
    :param TripKey: The name of the trip
    :return: renders template of the selected trip with detailed information
    """
    tripDetails, meta, ParticpantInfo = db.getTrip(TripKey)
    print(tripDetails)
    print(meta)
    print(ParticpantInfo)
    return render_template("TripPage.html", Tripinfo=tripDetails[0], TripMeta=meta[0], ParticpantInfo= ParticpantInfo)


@main.route('/addTrip', methods=['POST','GET'])
def add_Trip():
    form = MakeTripFormPOA()
    if request.method == 'POST':
        # print(form.data)  # returns a dictonary with keys that are the feilds in the table
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('CreateTrip.html', form=form)
        else:
            db.AddTrip(form.data)
            flash('New entry was successfully posted')
            return redirect(url_for('main.Main'))#Im going to be honest this naming schema is terible
    elif request.method == 'GET':
        return render_template('CreateTrip.html', form=form)


@main.route('/addParticipant/<FormKey>',  methods=['POST','GET'])
def add_Participant(FormKey):
    tripname = db.cursor.execute('select Trip_Name, Participant_num, Partcipant_cap, id from'
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
            return redirect(url_for('main.TripPage', TripKey=str(FormKey)))

@main.route('/login', methods=['POST', 'GET'])
def login():
    if 'credentials' not in flask.session:#are they already authenticated if not go to authentication
        return flask.redirect(flask.url_for('main.gCallback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:#if the acess token is expired ask them to reauthenticate
        return flask.redirect(flask.url_for('main.gCallback'))
    else:#if authenticated get user info
        http_auth = credentials.authorize(httplib2.Http())
        service = google.discovery.build('oauth2', 'v2', http_auth)#we ask for there profile information
        userinfo = service.userinfo().get().execute()#execute requst
        print(userinfo)
        return json.dumps(userinfo)


@main.route('/deleteParicipant/<id>')
def remove_particpant(id):
    tripKey = db.cursor.execute('select Trips_Key from Participants where id=' + id).fetchall()[0][0]
    db.deleteParticpant(id)
    return redirect(url_for('main.TripPage', TripKey=tripKey))


