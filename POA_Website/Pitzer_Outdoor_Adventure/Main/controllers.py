from Forms.POAForms import MakeTripFormPOA, AddToTripPOA, EditTripMemberPOA, CreateAccountForm, ModifyAccountForm
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
def mainPage():
    """
    The main page of the website.
    :return: 
    """
    masters = Master.query.checkTrip()
    # print(masters[0].Car_Cap)
    #if 'Googledata' in flask.session:
    #    flask.session.pop('Googledata', None)
    #if 'credentials' in flask.session:
    #    flask.session.pop('credentials', None)
    return render_template("HomePage.html", entries=masters)


@main.route("/trips/<int:TripKey>")
def tripPage(TripKey):
    """
    Finds a specific trip and displays it on screen.
    :param TripKey: The name of the trip
    :return: renders template of the selected trip with detailed information
    """
    # FINISHED: MAKE YOUR METERBARS AND JOIN TRIP BUTTON IN A SIDEBAR TOGETHER! This would look really cool.
    meta = Master.query.filter_by(id=TripKey).first()  # Returns a 1 element list lets get the object from that
    tripDetails = Trips.query.filter_by(Master_Key=TripKey).first()
    participantInfo = Participants.query.filter_by(Master_Key=TripKey).all()
    coordinator = Participants.query.filter_by(Master_Key=TripKey, Leader=True).first()
    if 'credentials' in flask.session and 'Googledata' in flask.session:
        userID = flask.session['Googledata']['id'][:]
    else:
        userID = ''
    onTrip = False
    for those in participantInfo:
        if those.accountID == userID:
            onTrip = True
    # Check whether the current user, if they're logged in, is a coordinator.
    if coordinator.accountID == userID:
        youAreCoordinator = True
    else:
        youAreCoordinator = False
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
    # FINISHED: Add a button at the top called "Leave Trip" which removes you from this trip if you are on it.
    # ^^^ Wait! Do we want the coordinator to be able to boot people from trips? Shouldn't they retain the original menu format?
    # ^^ ALASDAIR: NO WE DO NOT, THAT SHOULD BE A POWER RESERVED FOR ADMINISTRATORS.
    return render_template("TripPage.html", Tripinfo=tripDetails, TripMeta=meta, Coordinator=coordinator, ParticipantInfo=participantInfo, participantRatio=participantRatio, carRatio=carRatio, userID=userID, onTrip=onTrip, youAreCoordinator=youAreCoordinator)


@main.route('/addTrip', methods=['POST','GET'])
@login_required
def addTrip():
    """
    Sends the user a form to fill out with trip information, then makes a new trip using that data.
    :return: 
    """
    tempUser = Account.query.filter_by(id=flask.session['Googledata']['id']).first()
    form = MakeTripFormPOA(Car_Capacity=str(tempUser.carCapacity))
    # FINISHED: Make the above form autofill the car capacity with the user's data. WAIT, WHAT DOES THIS MEAN? THAT'S NEVER REQUESTED IN THE FORM!(?)
    if request.method == 'POST':
        # print(form.data)  # Returns a dictionary with keys that are the fields in the table.
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('CreateTripModal.html', form=form)
        else:
            newSeats = int(form.data["Car_Capacity"][:])
            if form.data["Driver"] == False:
                newSeats = 0
            model = TripModel(form.data, tempUser)
            Participants.query.addParticipant(tempUser, form.data["Driver"], newSeats, model.master.id, True, False)
            model.addModel() # add trip to db
            db.session.commit()
            flash('New entry was successfully posted')
            return redirect(url_for('main.mainPage')) # I'm going to be honest, this naming schema is terrible. MATTHEW: FIXED SO IT'S NO LONGER TERRIBLE!
    elif request.method == 'GET':
        return render_template('CreateTripModal.html', form=form)


@main.route('/addParticipant/<FormKey>',  methods=['POST','GET'])
@login_required
def addParticipant(FormKey):
    """
    Adds a participant to a trip.
    :param FormKey: 
    :return: 
    """
    tempUser = Account.query.filter_by(id=flask.session['Googledata']['id']).first()
    tripInfo = Master.query.filter_by(id=FormKey).first()
    # Could be made more efficient by only querying for trip name.
    # if tempUser.carCapacity != 0:
    form = AddToTripPOA(Driver=False, Car_Capacity=str(tempUser.carCapacity))
    if request.method == 'GET':
        if 0 != len(Participants.query.filter_by(Master_Key=FormKey).all()) and (tripInfo.Participant_Cap <= tripInfo.Participant_Num and tripInfo.Car_Cap <= tripInfo.Car_Num):
            # You cannot join the trip, no buts about it.
            # FINISHED: FLASH A THING ON THE SCREEN
            # vvv Make this render a new modal-type template, just like you did earlier but with only a warning message saying the trip is full. DID IT, FINISHED!!!!
            return render_template('DisplayMessageModal.html', message="Sorry, there's no room left on this trip.", title="Trip is Full")
            #redirect(url_for("main.tripPage", FormKey=str(FormKey)))
        else:
            return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, warning=False, errorMessage="")
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, warning=False, errorMessage="")
        else:
            newSeats = int(form.data["Car_Capacity"][:])
            isDriver = form.data["Driver"]
            # Makes the number of seats and driver status consistent.
            if form.data["Driver"] == False:
                newSeats = 0
            if newSeats == 0:
                isDriver = False
            if isDriver and tripInfo.Car_Num + 1 > tripInfo.Car_Cap:
                # The person is trying to be a driver when the trip already has maximum/over maximum cars.
                return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, warning=True, errorMessage="There are already too many cars on this trip; you cannot be a driver if you want to join.")
            if newSeats <= 0 and tripInfo.Participant_Num >= tripInfo.Participant_Cap:
                # The person has zero newSeats and tries to join a trip with maximum/over maximum people
                # You are forced to be a driver.
                # You can be a driver even on overloaded trips, as long as you have at least one car capacity. After all, you're not hurting anyone by taking up space, right?
                return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, warning=True, errorMessage="Due to the current size of this trip, you must be a driver with at least one car capacity to join.")
            # Congratulations! You submitted your form and all fields were filled out properly.
            # I DON'T THINK YOU NEED checkAddParticipant, YOU CAN JUST RUN YOUR CHECKS HERE AND IF THEY DON'T FIT THEN YOU CAN REJECT THE USER.
            Participants.query.addParticipant(tempUser, isDriver, newSeats, int(FormKey), False, False)
            # FINISHED: Make sure you can only remove yourself from a trip.
            # Should you be able to add yourself multiple times to a trip?
            # ^^ ALASDAIR: NO YOU SHOULD NOT.
            # ^^^ Wait! Do we want the coordinator to be able to boot people from trips? Shouldn't they retain the original menu format?
            # ^^ ALASDAIR: NO WE DO NOT, THAT SHOULD BE A POWER RESERVED FOR ADMINISTRATORS.
            # WHEN YOU EXIT A TRIP, YOU TAKE YOUR CAR WITH YOU! WILL/SHOULD THAT THROW PEOPLE OFF THE TRIP?!?
            # ^^ ALASDAIR: MAKE IT SO THAT IT PUTS UP A WARNING, AND PREVENTS NON-DRIVERS FROM JOINING. (if you're a driver and still can't push above the participant cap, that's okay because at least your're helping.)
            flash('New entry was successfully posted')
            return redirect(url_for('main.tripPage', TripKey=str(FormKey)))
    # else:
    # Participants.query.addParticipant(tempUser, False, int(FormKey))
    # flash('New entry was successfully posted')
    # return redirect(url_for('main.tripPage', TripKey=str(FormKey)))

@main.route('/editParticipant/<FormKey>',  methods=['POST','GET'])
@login_required
def editParticipant(FormKey):
    you = Participants.query.filter_by(accountID=flask.session['Googledata']['id'], Master_Key=FormKey).first()
    tripInfo = Master.query.filter_by(id=FormKey).first()
    form = EditTripMemberPOA(Driver_Box=you.Driver, CarCapacity_Box=str(you.Car_Capacity), PotentialLeader_Box=you.OpenLeader)
    if request.method == 'GET':
        return render_template('EditTripMemberModal.html', form=form, tripInfo=tripInfo, warning=False, errorMessage="")
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('EditTripMemberModal.html', form=form, tripInfo=tripInfo, warning=False, errorMessage="")
        else:
            newSeats = int(form.data["CarCapacity_Box"][:])
            isDriver = form.data["Driver_Box"]
            # Makes the number of seats and driver status consistent.
            if form.data["Driver_Box"] == False:
                newSeats = 0
            if newSeats == 0:
                isDriver = False
            # Congratulations! You submitted your form and all fields were filled out properly.
            you.editParticipantInfo(isDriver, newSeats, form.data["PotentialLeader_Box"])
            db.session.commit()
            return redirect(url_for('main.tripPage', TripKey=str(FormKey)))

@main.route('/checkAddParticipant/<FormKey>',  methods=['POST','GET'])
@login_required
def checkAddParticipant(FormKey):
    """
    Checks to see whether a new participant can fit in a trip.
    :param FormKey: 
    :return: 
    """
    tempTrip = Master.query.filter_by(id=FormKey).first()
    tempUser = Account.query.filter_by(id=flask.session['Googledata']['id']).first()
    if tempTrip.Participant_Cap < tempTrip.Participant_Num + 1 and tempTrip.Car_Cap < tempTrip.Car_Num + 1:
        # You cannot join the trip, no buts about it.
        # TODO: FLASH A THING ON THE SCREEN
        return redirect(url_for("main.tripPage", FormKey=str(FormKey)))
    else:
        # You can join, no problem!
        return redirect(url_for("main.addParticipant", FormKey=str(FormKey)))
    #memes
    # elif tempTrip.Participant_Cap + tempUser.carCapacity >= tempTrip.Participant_Num + 1 and tempTrip.Participant_Cap < tempTrip.Participant_Num + 1:
    #     # You are forced to be a driver.
    #     return redirect(url_for("main.addParticipant", FormKey=str(FormKey)))

@main.route('/login', methods=['POST', 'GET'])
def login():
    """
    Retrieves the user's data from Google through gCallback, then has the user either make an account or go to the main page.
    :return: 
    """
    if 'credentials' not in flask.session: # Are they already authenticated? If not, then go to authentication.
        return flask.redirect(flask.url_for('main.gCallback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired: # If the access token is expired, ask them to re-authenticate.
        return flask.redirect(flask.url_for('main.gCallback'))
    else: # If authenticated, get user info.
        http_auth = credentials.authorize(httplib2.Http())
        service = google.discovery.build('oauth2', 'v2', http_auth)  # We ask for their profile information.
        userinfo = service.userinfo().get().execute()  # Execute request.
        #print(userinfo)

        #populate form with google data
        flask.session['Googledata'] = userinfo
        #print(flask.session)
        #return rendertemplate(create acoubt.html, form=form)
        #Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum
        #if flask.session['Googledata']['id']==Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum:
        if None == Account.query.filter_by(id=flask.session['Googledata']['id']).first():
            return redirect(url_for('main.makeAccount'))
        else:
            return redirect(url_for('main.mainPage'))

@main.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    """
    Dumps the user's Googledata and credentials.
    :return: 
    """
    flask.session.pop('Googledata', None)
    flask.session.pop('credentials', None)
    return redirect(url_for('main.mainPage'))

@main.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    """
    Directs the user to their profile page, where their account information is displayed.
    :return: 
    """
    # print(Account.query.filter_by(id=flask.session['Googledata']['id']).first().accessData()['picture'])
    tempTime = datetime.today()
    # print(tempTime.strftime('%B'))
    # https://docs.python.org/2/library/datetime.html#module-datetime
    # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    return render_template("ProfilePage.html", user=Account.query.filter_by(id=flask.session['Googledata']['id']).first(), time=tempTime)

@main.route('/createAccount', methods=['POST', 'GET'])
def makeAccount():
    """
    This constructs a new account from the user's information.
    :return: 
    """
    #Account.query.filter_by(id=flask.session['Googledata']['id']).first().googleNum
    if 'credentials' not in flask.session or 'Googledata' not in flask.session:
        return redirect(url_for('main.mainPage'))
    if None != Account.query.filter_by(id=flask.session['Googledata']['id']).first():
        return redirect(url_for('main.mainPage'))
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
                return redirect(url_for('main.mainPage'))
        elif request.method == 'GET':
            return render_template("NewAccount.html", form=form)

@main.route('/editAccount', methods=['POST', 'GET'])
@login_required
def editAccount():
    """
    This edits the user's account information.
    :return: 
    """
    #print('made it to stage one')
    if None == Account.query.filter_by(id=flask.session['Googledata']['id']).first():
        #print('took a wrong turn')
        return redirect(url_for('main.mainPage'))
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
                #print(form.data)
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
                selectedUser = Account.query.filter_by(id=flask.session['Googledata']['id']).first()
                selectedUser.modifyAccount(packedInfo)
                tripSelves = Participants.query.filter_by(accountID=flask.session['Googledata']['id']).all()
                for those in tripSelves:
                    those.changeUserInfo(selectedUser)
                db.session.commit()
                # Fixed! Now account changes are permanent.  =)
                #print(Account.query.all())
                #print(Account.query.all()[0].accessData())
                return redirect(url_for('main.profile'))
        elif request.method == 'GET':
            return render_template("ModifyAccount.html", form=form)

@main.route('/gCallback')
def gCallback():
    """
    This handles authentication. Granted, we're not quite sure how... but it does.
    :return:
    """
    secret = os.path.join(main.root_path[:-29], 'secret/client_secret.json') #access the secret file
    #the -29 changes path yo POA Website rather than the path to mainPage
    flow = client.flow_from_clientsecrets(secret, scope='https://www.googleapis.com/auth/userinfo.profile', redirect_uri=flask.url_for('main.gCallback', _external=True))
     # ,include_granted_scopes=True)
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url() #sends request to google which redirects user to sign in
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code') #we have received a token form a user
        credentials = flow.step2_exchange(auth_code) #authenticate that token with google
        flask.session['credentials'] = credentials.to_json() #we have authenticated the user
        return flask.redirect(flask.url_for('main.login')) #once authenticated return to main page

@main.route('/cannotLeave')
def cannotLeave():
    return render_template('DisplayMessageModal.html', message="You are this trip's coordinator. You cannot leave until you have passed the role onto someone else.", title="Cannot Leave Trip")

@main.route('/deleteParticipant/<personID>/<tripID>')
def removeParticipant(personID, tripID):
    Participants.query.removeParticipant(personID, tripID)
    return redirect(url_for('main.tripPage', TripKey=tripID))

@main.route('/swapCoordinators/<oldLeaderID>/<newLeaderID>/<tripID>')
def swapCoordinators(oldLeaderID, newLeaderID, tripID):
    oldLeader = Participants.query.filter_by(accountID=oldLeaderID, Master_Key=tripID).first()
    newLeader = Participants.query.filter_by(accountID=newLeaderID, Master_Key=tripID).first()
    oldLeader.Leader = False
    oldLeader.OpenLeader = False
    newLeader.Leader = True
    newLeader.OpenLeader = False
    return redirect(url_for('main.tripPage', TripKey=tripID))

# tempParticipant = Participants.query.filter_by(id=int(theID))
# tripKey = tempParticipant.first().Master_Key
# tempMaster = Master.query.filter_by(id=int(tripKey)).first()
# tempMaster.Participant_Num -= 1
# if tempParticipant.first().Driver == 1:  # What is going on with this check? Isn't Driver a boolean?
#     tempMaster.Car_Num -= 1
# tempParticipant.delete()
# db.session.commit()
# return redirect(url_for('main.tripPage', TripKey=tripKey))