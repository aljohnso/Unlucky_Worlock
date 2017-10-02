# from Tests.protyping.UserAccounts import db, Account, databaseName, currentPath, createAccount
# from Tests.TestForms.SecondForms import CreateAccountForm
import flask
from flask import request, redirect, url_for, \
    render_template, flash, Blueprint

from DatabaseConnection.DataBaseSchema import db, \
    Master, Participants, TripModel, Account
from Forms.POAForms import MakeTripFormPOA, AddToTripPOA, EditTripMemberPOA
from Pitzer_Outdoor_Adventure.Main.controllers import login_required

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/popUpMessage/<title>/<message>', methods=['GET', 'POST'])
def popUpMessage(title, message):
    """
    Displays a pop-up message.
    :param title:
    :param message:
    :return:
    """
    return render_template("DisplayMessageModal.html", message=message, title=title)


@api.route('/addTrip', methods=['POST', 'GET'])
@login_required
def addTrip():
    """
    Sends the user a form to fill out with trip information, then makes a new trip using that data.
    :return:
    """
    tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
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
            model.addModel()  # add trip to db
            db.session.commit()
            flash('New entry was successfully posted')
            return redirect(url_for('main.mainPage'))  # I'm going to be honest, this naming schema is terrible. MATTHEW: FIXED SO IT'S NO LONGER TERRIBLE!
    elif request.method == 'GET':
        return render_template('CreateTripModal.html', form=form)


@api.route('/addParticipant/<FormKey>', methods=['POST', 'GET'])
@login_required
def addParticipant(FormKey):
    """
    Adds a participant to a trip.
    :param FormKey:
    :return:
    """
    tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
    tripInfo = Master.query.filter_by(id=FormKey).first()
    # Could be made more efficient by only querying for trip name.
    # if tempUser.carCapacity != 0:
    form = AddToTripPOA(Driver=False, Car_Capacity=str(tempUser.carCapacity))
    if request.method == 'GET':
        if 0 != len(Participants.query.filter_by(Master_Key=FormKey).all()) and (
                tripInfo.Participant_Cap <= tripInfo.Participant_Num and tripInfo.Car_Cap <= tripInfo.Car_Num):
            # You cannot join the trip, no buts about it.
            # FINISHED: FLASH A THING ON THE SCREEN
            # Make this render a new modal-type template, just like you did earlier but with only a warning message saying the trip is full. DID IT, FINISHED!!!!
            return render_template('DisplayMessageModal.html', message="Sorry, there's no room left on this trip.", title="Trip is Full")
            # redirect(url_for("main.tripPage", FormKey=str(FormKey)))
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
                return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, warning=True,
                                       errorMessage="There are already too many cars on this trip; you cannot be a driver if you want to join.")
            if newSeats <= 0 and tripInfo.Participant_Num >= tripInfo.Participant_Cap:
                # The person has zero newSeats and tries to join a trip with maximum/over maximum people
                return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, warning=True,
                                       errorMessage="Due to the current size of this trip, you must be a driver with at least one car capacity to join.")
            Participants.query.addParticipant(tempUser, isDriver, newSeats, int(FormKey), False, False)
            flash('New entry was successfully posted')
            return redirect(url_for('main.tripPage', TripKey=str(FormKey)))


@api.route('/editParticipant/<FormKey>', methods=['POST', 'GET'])
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


@api.route('/checkAddParticipant/<FormKey>', methods=['POST', 'GET'])
@login_required
def checkAddParticipant(FormKey):
    """
    Checks to see whether a new participant can fit in a trip.
    :param FormKey:
    :return:
    """
    tempTrip = Master.query.filter_by(id=FormKey).first()
    tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
    if tempTrip.Participant_Cap < tempTrip.Participant_Num + 1 and tempTrip.Car_Cap < tempTrip.Car_Num + 1:
        # You cannot join the trip, no buts about it.
        # TODO: FLASH A THING ON THE SCREEN
        return redirect(url_for("main.tripPage", FormKey=str(FormKey)))
    else:
        # You can join, no problem!
        return redirect(url_for("main.addParticipant", FormKey=str(FormKey)))


@api.route('/tripDisplay')
@login_required
def tripDisplay():
    listOfParticipants = Participants.query.filter_by(accountID=flask.session['Googledata']['id']).all()
    listOfTrips = []
    for those in listOfParticipants:
        listOfTrips.append(Master.query.filter_by(id=those.Master_Key).first())
    return render_template('DisplayTripsModal.html', listOfTrips=listOfTrips)

@api.route('/cannotLeave')
def cannotLeave():
    return render_template('DisplayMessageModal.html', message="You are this trip's coordinator. You cannot leave until you have passed the role onto someone else.", title="Cannot Leave Trip")


@api.route('/deleteParticipant/<personID>/<tripID>')
def removeParticipant(personID, tripID):
    Participants.query.removeParticipant(personID, tripID)
    return redirect(url_for('main.tripPage', TripKey=tripID))


@api.route('/swapCoordinators/<oldLeaderID>/<newLeaderID>/<tripID>')
def swapCoordinators(oldLeaderID, newLeaderID, tripID):
    Participants.query.swapCordinator(oldLeaderID, newLeaderID, tripID)
    return redirect(url_for('main.tripPage', TripKey=tripID))