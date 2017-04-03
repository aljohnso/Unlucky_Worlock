from Forms.POAForms import MakeTripFormPOA, AddToTripPOA
from flask import  request, redirect, url_for, \
     render_template, flash,Blueprint
from DatabaseConnection.DataBaseSchema import db, \
    Master, Participants, TripModel, Trips
import json, flask, httplib2
import apiclient as google
from oauth2client import client
import os
main = Blueprint('main', __name__, template_folder='templates')


@main.route('/', methods=['GET', 'POST'])
def Main():
    masters = Master.query.checkTrip()
    # print(masters[0].Car_Cap)
    return render_template("HomePage.html", entries=masters)


@main.route("/trips/<int:TripKey>")
def TripPage(TripKey):
    """
    :param TripKey: The name of the trip
    :return: renders template of the selected trip with detailed information
    """
    meta = Master.query.filter_by(id=TripKey).first()  # returns a 1 element list lets get the object from that
    tripDetails = Trips.query.filter_by(Master_Key=TripKey).first()
    ParticpantInfo = Participants.query.filter_by(Master_Key=TripKey).all()
    print(tripDetails)
    print(meta)
    print(ParticpantInfo)
    return render_template("TripPage.html", Tripinfo=tripDetails, TripMeta=meta, ParticpantInfo=ParticpantInfo)


@main.route('/addTrip', methods=['POST','GET'])
def add_Trip():
    form = MakeTripFormPOA()
    if request.method == 'POST':
        # print(form.data)  # returns a dictonary with keys that are the feilds in the table
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('CreateTrip.html', form=form)
        else:
            model = TripModel(form.data)
            model.addModel()  # add trip to db
            db.session.commit()
            flash('New entry was successfully posted')
            return redirect(url_for('main.Main'))  # Im going to be honest this naming schema is terible
    elif request.method == 'GET':
        return render_template('CreateTrip.html', form=form)


@main.route('/addParticipant/<FormKey>',  methods=['POST','GET'])
def add_Participant(FormKey):
    tripname = Master.query.filter_by(id=FormKey).all()[0]
    # Could be made more efficent by only querying for trip name
    form = AddToTripPOA()
    if request.method == 'GET':
        return render_template('Add_Particpant.html', form=form, tripname=tripname)
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('Add_Particpant.html', form=form, tripname=tripname)
        else:
            particpant = Participants(form.data, int(FormKey))
            db.session.add(particpant)
            master = Master.query.filter_by(id = int(FormKey)).first()
            master.Participant_num += 1
            if particpant.Driver == 1:
                master.Car_Num += 1
            db.session.commit()
            flash('New entry was successfully posted')
            return redirect(url_for('main.TripPage', TripKey=str(FormKey)))

@main.route('/login', methods=['POST', 'GET'])
def login():
    if 'credentials' not in flask.session:  # are they already authenticated if not go to authentication
        return flask.redirect(flask.url_for('main.gCallback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:  # if the acess token is expired ask them to reauthenticate
        return flask.redirect(flask.url_for('main.gCallback'))
    else:  # if authenticated get user info
        http_auth = credentials.authorize(httplib2.Http())
        service = google.discovery.build('oauth2', 'v2', http_auth)  # we ask for there profile information
        userinfo = service.userinfo().get().execute()  # execute requst
        print(userinfo)
        return json.dumps(userinfo)


@main.route('/gCallback')
def gCallback():
    """
    This handels authentication not quite sure how but it does
    :return:
    """
    secret = os.path.join(main.root_path[:-29], 'secret/client_secret.json')#access the secret file
    #the -29 changes path yo POA Website rather than the path to Main
    flow = client.flow_from_clientsecrets(secret, scope='https://www.googleapis.com/auth/userinfo.profile',
                                          redirect_uri=flask.url_for('main.gCallback', _external=True))
     # ,include_granted_scopes=True)
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()#sends request to google which redircects user to sign in
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')#we have recived a token form a user
        credentials = flow.step2_exchange(auth_code)#authenticate that token with google
        flask.session['credentials'] = credentials.to_json()#we have authenticated the user
        return flask.redirect(flask.url_for('main.login'))#once authenticated return to main page





@main.route('/deleteParicipant/<id>')
def remove_particpant(id):
    paricipant = Participants.query.filter_by(id=int(id))
    tripKey = paricipant.all()[0].Master_Key
    master = Master.query.filter_by(id=int(tripKey )).first()
    master.Participant_num -= 1
    if paricipant.first().Driver == 1:
        master.Car_Num -= 1
    paricipant.delete()
    db.session.commit()
    return redirect(url_for('main.TripPage', TripKey=tripKey))


