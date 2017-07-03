from Forms.POAForms import MakeTripFormPOA, AddToTripPOA, CreateAccountForm, ModifyAccountForm
from flask import  request, redirect, url_for, \
     render_template, flash, Blueprint, session
from DatabaseConnection.DataBaseSchema import db, \
    Master, Participants, TripModel, Trips, Account, createAccount
#from Tests.protyping.UserAccounts import db, Account, databaseName, currentPath, createAccount
#from Tests.TestForms.SecondForms import CreateAccountForm
from functools import wraps
import json, flask, httplib2
import apiclient as google
from oauth2client import client
from datetime import datetime

import os
main = Blueprint('main', __name__, template_folder='templates')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'credentials' not in flask.session or 'Googledata' not in flask.session:
            return redirect(url_for('main.login'))
        elif None == Account.query.filter_by(id=flask.session['Googledata']['id']).first():
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/', methods=['GET', 'POST'])
def Main():
    masters = Master.query.checkTrip()
    # print(masters[0].Car_Cap)
    #if 'Googledata' in flask.session:
    #    flask.session.pop('Googledata', None)
    #if 'credentials' in flask.session:
    #    flask.session.pop('credentials', None)
    return render_template("HomePage.html", entries=masters)


@main.route("/trips/<int:TripKey>")
def TripPage(TripKey):
    """
    :param TripKey: The name of the trip
    :return: renders template of the selected trip with detailed information
    """
    meta = Master.query.filter_by(id=TripKey).first()  # Returns a 1 element list lets get the object from that
    tripDetails = Trips.query.filter_by(Master_Key=TripKey).first()
    ParticipantInfo = Participants.query.filter_by(Master_Key=TripKey).all()
    #print(tripDetails)
    #print(meta)
    #print(ParticpantInfo)
    if int(round(meta.Participant_Cap))==0:
        participantRatio = "100"
    else:
        participantRatio = str(round(100 * float(meta.Participant_Num)/float(meta.Participant_Cap)))
    if int(round(meta.Car_Cap)) == 0:
        carRatio = "100"
    else:
        carRatio = str(round(100 * float(meta.Car_Num)/float(meta.Car_Cap)))
    if int(participantRatio) < 0:
        participantRatio = "0"
    elif int(participantRatio) > 100:
        participantRatio = "100"
    if int(carRatio) < 0:
        carRatio = "0"
    elif int(carRatio) > 100:
        carRatio = "100"
    # TODO: Add a button at the top called "Leave Trip" which removes you from this trip if you are on it.
    # ^^^ Wait! Do we want the coordinator to be able to boot people from trips? Shouldn't they retain the original menu format?
    return render_template("TripPage.html", Tripinfo=tripDetails, TripMeta=meta, ParticipantInfo=ParticipantInfo, participantRatio=participantRatio, carRatio=carRatio)


@main.route('/addTrip', methods=['POST','GET'])
@login_required
def add_Trip():
    tempUser = Account.query.filter_by(id=flask.session['Googledata']['id']).first()
    form = MakeTripFormPOA()
    # TODO: Make the above form autofill the car capacity with the user's data. WAIT, WHAT DOES THIS MEAN? THAT'S NEVER REQUESTED IN THE FORM!(?)
    if request.method == 'POST':
        # print(form.data)  # Returns a dictionary with keys that are the fields in the table.
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('CreateTrip.html', form=form)
        else:
            model = TripModel(form.data, tempUser)
            model.addModel() # add trip to db
            db.session.commit()
            flash('New entry was successfully posted')
            return redirect(url_for('main.Main')) # I'm going to be honest, this naming schema is terrible.
    elif request.method == 'GET':
        return render_template('CreateTrip.html', form=form)


@main.route('/addParticipant/<FormKey>',  methods=['POST','GET'])
@login_required
def addParticipant(FormKey):
    tempUser = Account.query.filter_by(id=flask.session['Googledata']['id']).first()
    tripInfo = Master.query.filter_by(id=FormKey).all()[0]
    # Could be made more efficient by only querying for trip name.
    # if tempUser.carCapacity != 0:
    form = AddToTripPOA(Car_Capacity=str(tempUser.carCapacity))
    if request.method == 'GET':
        return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo)
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo)
        else:
            Participants.query.addParticipant(tempUser, form.data["Driver"], int(FormKey))
            # TODO: Make sure you can only remove yourself from a trip.
            # TODO: Should you be able to add yourself multiple times to a trip?
            # ^^^ Wait! Do we want the coordinator to be able to boot people from trips? Shouldn't they retain the original menu format?
            flash('New entry was successfully posted')
            return redirect(url_for('main.TripPage', TripKey=str(FormKey)))
    # else:
    # Participants.query.addParticipant(tempUser, False, int(FormKey))
    # flash('New entry was successfully posted')
    # return redirect(url_for('main.TripPage', TripKey=str(FormKey)))

@main.route('/checkAddParticipant/<FormKey>',  methods=['POST','GET'])
@login_required
def checkAddParticipant(FormKey):
    tempTrip = Master.query.filter_by(id=FormKey).all()[0]
    tempUser = Account.query.filter_by(id=flask.session['Googledata']['id']).first()
    if tempTrip.Participant_Cap < tempTrip.Participant_Num + 1 and tempTrip.Car_Cap < tempTrip.Car_Num + 1:
        # You cannot join the trip, no buts about it.
        # FLASH A THING ON THE SCREEN
        return redirect(url_for("main.addParticipant", FormKey=str(FormKey)))
    elif tempTrip.Participant_Cap + tempUser.carCapacity >= tempTrip.Participant_Num + 1 and tempTrip.Participant_Cap < tempTrip.Participant_Num + 1:
        # You are forced to be a driver.
        return redirect(url_for("main.addParticipant", FormKey=str(FormKey)))
    else:
        # You can join, no problem!
        return redirect(url_for("main.addParticipant", FormKey=str(FormKey)))

@main.route('/login', methods=['POST', 'GET'])
def login():
    if 'credentials' not in flask.session:  # are they already authenticated if not go to authentication
        return flask.redirect(flask.url_for('main.gCallback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:  # if the access token is expired ask them to reauthenticate
        return flask.redirect(flask.url_for('main.gCallback'))
    else:  # if authenticated get user info
        http_auth = credentials.authorize(httplib2.Http())
        service = google.discovery.build('oauth2', 'v2', http_auth)  # we ask for there profile information
        userinfo = service.userinfo().get().execute()  # execute requst
        print(userinfo)

        #populate form with google data
        flask.session['Googledata'] = userinfo
        print(flask.session)
        #return rendertemplate(create acoubt.html, form=form)
        #Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum
        #if flask.session['Googledata']['id']==Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum:
        if None != Account.query.filter_by(id=flask.session['Googledata']['id']).first():
            return redirect(url_for('main.Main'))
        else:
            return redirect(url_for('main.makeAccount'))

@main.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    flask.session.pop('Googledata', None)
    flask.session.pop('credentials', None)
    return redirect(url_for('main.Main'))

@main.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    # print(Account.query.filter_by(id=flask.session['Googledata']['id']).first().accessData()['picture'])
    tempTime = datetime.today()
    # print(tempTime.strftime('%B'))
    # https://docs.python.org/2/library/datetime.html#module-datetime
    # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    return render_template("ProfilePage.html", user=Account.query.filter_by(id=flask.session['Googledata']['id']).first(), time=tempTime)

@main.route('/createAccount', methods=['POST', 'GET'])
def makeAccount():
    #Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum
    if 'credentials' not in flask.session or 'Googledata' not in flask.session:
        return redirect(url_for('main.Main'))
    if None != Account.query.filter_by(id=flask.session['Googledata']['id']).first():
        return redirect(url_for('main.Main'))
    else:
        form = CreateAccountForm(FirstName_Box=flask.session['Googledata']["given_name"][:], LastName_Box=flask.session['Googledata']["family_name"][:])
        #TODO: Remove Googledata from session if you can, but doing this isn't that important.
        if request.method == 'POST':
            # print(form.data)  # returns a dictionary with keys that are the fields in the table
            if form.validate_on_submit() == False:
                flash('All fields are required.')
                return render_template("NewAccount.html", form=form)
            else:
                flash('New entry was successfully posted')
                print(form.data)
                userinfo = {
                    'googleNum': flask.session['Googledata']['id'][:],
                    'picture': flask.session['Googledata']['picture'][:],
                    'username': str(form.data['FirstName_Box'][:] + ' ' + form.data['LastName_Box'][:]),
                    'email': form.data['Email_Box'][:],
                    'firstName': form.data['FirstName_Box'][:],
                    'lastName': form.data['LastName_Box'][:],
                    'age': str(form.data['Age_Box'])[:],
                    'height': str(form.data['Height_Box'])[:],
                    'allergies': 'TBD',
                    'dietRestrictions': 'TBD',
                    'studentIDNumber': str(form.data['StudentIDNumber_Box'])[:],
                    'phoneNumber': str(form.data['PhoneNumber_Box'])[:],
                    'carCapacity': str(form.data['CarCapacity_Box'])[:],
                    'locale': flask.session['Googledata']['locale'][:],
                }
                # # unpackedInfo = form.data["FirstName_Box"]
                packedInfo = json.dumps(userinfo)
                # First Pass form to class that parse to dict that can be passed to createAccount
                # create the createAcount object and add it to the session then commit
                # EXTRA CREDIT make a page to edit account info
                createAccount(packedInfo)
                # temp = createAccount(packedInfo)
                # temp = Account(form.data['Sample_Box'], "spam", 10000)
                # db.session.add(temp)
                # db.session.commit()
                print(Account.query.all())
                print(Account.query.all()[0].accessData())
                return redirect(url_for('main.Main'))
        elif request.method == 'GET':
            return render_template("NewAccount.html", form=form)

@main.route('/editAccount', methods=['POST', 'GET'])
@login_required
def editAccount():
    print('made it to stage one')
    if None == Account.query.filter_by(id=flask.session['Googledata']['id']).first():
        print('took a wrong turn')
        return redirect(url_for('main.Main'))
    else:
        currentData = Account.query.filter_by(id=flask.session['Googledata']['id']).first().accessData()
        form = ModifyAccountForm(FirstName_Box=currentData['firstName'][:], LastName_Box=currentData['lastName'][:], Email_Box=currentData['email'][:], Age_Box=currentData['age'][:], Height_Box=currentData['height'][:], StudentIDNumber_Box=currentData['studentIDNumber'][:], PhoneNumber_Box=currentData['phoneNumber'][:], CarCapacity_Box=currentData['carCapacity'][:])
        if request.method == 'POST':
            # print(form.data)  # returns a dictionary with keys that are the fields in the table
            if form.validate_on_submit() == False:
                flash('All fields are required.')
                return render_template("ModifyAccount.html", form=form)
            else:
                flash('Account was successfully modified')
                print(form.data)
                userinfo = {
                    'googleNum': flask.session['Googledata']['id'][:],
                    'picture': flask.session['Googledata']['picture'][:],
                    'username': str(form.data['FirstName_Box'][:] + ' ' + form.data['LastName_Box'][:]),
                    'email': str(form.data['Email_Box'][:]),
                    'firstName': str(form.data['FirstName_Box'][:]),
                    'lastName': str(form.data['LastName_Box'][:]),
                    'age': str(form.data['Age_Box'])[:],
                    'height': str(form.data['Height_Box'])[:],
                    'allergies': 'TBD',
                    'dietRestrictions': 'TBD',
                    'studentIDNumber': str(form.data['StudentIDNumber_Box'])[:],
                    'phoneNumber': str(form.data['PhoneNumber_Box'])[:],
                    'carCapacity': str(form.data['CarCapacity_Box'])[:],
                }
                # # unpackedInfo = form.data["FirstName_Box"]
                #THINGS TO ASK ALASDAIR
                # Do queries make copies of our users, or return the actual entries? (ask because of modifyAccount function)
                # Why does it not recognize the existence of Googledata here? How did it work in createAccount?
                packedInfo = json.dumps(userinfo)
                Account.query.filter_by(id=flask.session['Googledata']['id']).first().modifyAccount(packedInfo)
                db.session.commit()
                # Fixed! Now account changes are permanent.  =)
                print(Account.query.all())
                print(Account.query.all()[0].accessData())
                return redirect(url_for('main.profile'))
        elif request.method == 'GET':
            return render_template("ModifyAccount.html", form=form)

@main.route('/gCallback')
def gCallback():
    """
    This handles authentication, not quite sure how but it does.
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
    participant = Participants.query.filter_by(id=int(id))
    tripKey = participant.all()[0].Master_Key
    master = Master.query.filter_by(id=int(tripKey )).first()
    master.Participant_num -= 1
    if participant.first().Driver == 1:
        master.Car_Num -= 1
    participant.delete()
    db.session.commit()
    return redirect(url_for('main.TripPage', TripKey=tripKey))


