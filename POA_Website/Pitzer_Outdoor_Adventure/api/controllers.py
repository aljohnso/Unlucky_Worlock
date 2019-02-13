# from Tests.protyping.UserAccounts import db, Account, databaseName, currentPath, createAccount
# from Tests.TestForms.SecondForms import CreateAccountForm
import flask, datetime, re, copy
from flask import request, redirect, url_for, \
    render_template, flash, Blueprint, jsonify

from DatabaseConnection.DataBaseSchema import db, \
    Master, Trips, Participants, TripModel, Account
from Forms.POAForms import MakeTripFormPOA, AddToTripPOA, EditTripMemberPOA
from Pitzer_Outdoor_Adventure.Main.controllers import login_required
from flask_mail import Message, Mail
from Pitzer_Outdoor_Adventure.admin.controllers import admin_required
from flask_restful import Resource, Api
from Pitzer_Outdoor_Adventure.api.ApiHelpers import build_GET_return
mail = Mail()
#using decorators with flask_restful
#http://flask.pocoo.org/snippets/129/

# rewriting to crud
# all forms need to post to a crud path this could pose some issues for forms that use
# wtf forms but this tech is something I think we should move away from anyway
# Create
# Update
# Delete
# another problem is the ability to be able to make sure that users are authenticated
# also then if the user has a admin credential
# we could do some cool security stuff with salt and stuff and store the api keys
# I think I should purchs wifi lets see how much it is yeah that's to expensive
# Like wtf south west is so cheap comparatively


api_bp = Blueprint(name='api', import_name=__name__)
api = Api(api_bp)

class ApiAccount(Resource):
    """
        Account Api will deal with CRUD account operations
        Accounts are related to the account table. Accounts are used to
        Identify users in the system. These methods will allow user objects in the
        database to be modified
    """
    # @login_required
    def get(self, AccountID):
        """
        :param AccountID: primary key of account table
        :return: specific user id object
        """
        account_info = Account.query.filter_by(id=AccountID).first()
        return build_GET_return(account_info, recordName="Account")

    # @login_required
    # @admin_required
    # #So for this it appears from my mind that
    # def delete(self, todo_id):
    #     abort_if_todo_doesnt_exist(todo_id)
    #     del TODOS[todo_id]
    #     return '', 204
    #
    # def put(self, todo_id):
    #     args = parser.parse_args()
    #     task = {'task': args['task']}
    #     TODOS[todo_id] = task
    #     return task, 201

class ApiTrip(Resource):
    """
        This class will deal with modifing trips in the Master and Trip table
    """
    def get(self, tripID):
        """
        :param tripID: Master ID which is forieng key in trip table
        :return: Serialized version of trip and master table base of master ID
        """
        trip_table_info = Trips.query.filter_by(id=tripID).first().serialize
        master_table_info = Master.query.filter_by(id=tripID).first().serialize
        info = {"Master" : master_table_info, "Trips" : trip_table_info}
        return jsonify(status=200, body=info, recordName="Trip")

    def post(self):
        """
        Creates trip in DB
        :return: success hopefully
        """
        tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
        # Gathers the input from the form and stores it in a dictionary.
        data = request.form.to_dict()
        if "driver" in data:
            data["driver"] = True
        else:
            data["driver"] = False
        if "substanceFree" in data:
            data["substanceFree"] = True
        else:
            data["substanceFree"] = False
        data["departureDate"] = datetime.datetime.strptime(data["departureDate"], "%Y-%m-%d").date()
        data["returnDate"] = datetime.datetime.strptime(data["returnDate"], "%Y-%m-%d").date()
        costDict = {}
        tempKeys = copy.deepcopy(list(data.keys()))
        for entry in tempKeys:
            match = re.search("costName.*", entry)
            if match:
                costDict[data[entry]] = data["costMagnitude" + entry[8:]]
                data.pop(entry, None)
                data.pop("costMagnitude" + entry[8:], None)
        data["costDict"] = costDict
        print(data)
        newSeats = int(data["carCapacity"][:])
        if data["driver"] == False:
            newSeats = 0
        # change TripModel to use new syntax.
        model = TripModel(data, tempUser)
        Participants.query.addParticipant(tempUser, data["driver"], newSeats, model.master.id, True, False)
        model.addModel()  # add trip to db
        db.session.commit()
        flash('New entry was successfully posted')
        return jsonify(status="success", code=200)




api.add_resource(ApiAccount, '/Account/<int:AccountID>', methods=['GET'])

# @api_bp.route('/popUpMessage/<title>/<message>', methods=['GET', 'POST'])
# def popUpMessage(title, message):
#     """
#     Displays a pop-up message.
#     :param title:
#     :param message:
#     :return:
#     """
#     return render_template("DisplayMessageModal.html", message=message, title=title)
#
#
# @api_bp.route('/addTrip', methods=['POST', 'GET'])
# @login_required
# def addTrip():
#     """
#     Sends the user a form to fill out with trip information, then makes a new trip using that data.
#     :return:
#     """
#     tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
#     # FINISHED: Make the above form autofill the car capacity with the user's data. WAIT, WHAT DOES THIS MEAN? THAT'S NEVER REQUESTED IN THE FORM!(?)
#     if request.method == 'POST':
#         # Gathers the input from the form and stores it in a dictionary.
#         data = request.form.to_dict()
#         if "driver" in data:
#             data["driver"] = True
#         else:
#             data["driver"] = False
#         if "substanceFree" in data:
#             data["substanceFree"] = True
#         else:
#             data["substanceFree"] = False
#         data["departureDate"] = datetime.datetime.strptime(data["departureDate"], "%Y-%m-%d").date()
#         data["returnDate"] = datetime.datetime.strptime(data["returnDate"], "%Y-%m-%d").date()
#         costDict = {}
#         tempKeys = copy.deepcopy(list(data.keys()))
#         for entry in tempKeys:
#             match = re.search("costName.*", entry)
#             if match:
#                 costDict[data[entry]] = data["costMagnitude" + entry[8:]]
#                 data.pop(entry, None)
#                 data.pop("costMagnitude" + entry[8:], None)
#         data["costDict"] = costDict
#         print(data)
#         newSeats = int(data["carCapacity"][:])
#         if data["driver"] == False:
#             newSeats = 0
#         # change TripModel to use new syntax.
#         model = TripModel(data, tempUser)
#         Participants.query.addParticipant(tempUser, data["driver"], newSeats, model.master.id, True, False)
#         model.addModel()  # add trip to db
#         db.session.commit()
#         flash('New entry was successfully posted')
#         return jsonify(status="success", code=200)
#     elif request.method == 'GET': #TODO: move this route somewhere else its important
#         return render_template('CreateTripModal.html', yourCarCapacity=tempUser.carCapacity)

#
@api_bp.route('/addParticipant/<FormKey>', methods=['POST', 'GET'])
@login_required
def addParticipant(FormKey):
    """
    Adds a participant to a trip.
    :param FormKey:
    :return:
    """
    tripInfo = Master.query.filter_by(id=FormKey).first()
    tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
    # Could be made more efficient by only querying for trip name.
    # if tempUser.carCapacity != 0:
    form = AddToTripPOA(Driver=False, Car_Capacity=str(tempUser.carCapacity))
    if request.method == 'GET':
        if 0 != len(Participants.query.filter_by(Master_Key=FormKey).all()) and (
                tripInfo.Participant_Cap <= tripInfo.Participant_Num and tripInfo.Car_Cap <= tripInfo.Car_Num):
            # You cannot join the trip, no buts about it.
            # Make this render a new modal-type template, just like you did earlier but with only a warning message saying the trip is full. DID IT, FINISHED!!!!
            return render_template('DisplayMessageModal.html', message="Sorry, there's no room left on this trip.", title="Trip is Full")
            # redirect(url_for("main.tripPage", FormKey=str(FormKey)))
        else:
            return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, errorMessage="")
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, errorMessage="")
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
                return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, errorMessage="There are already too many cars on this trip; you cannot be a driver if you want to join.")
            if newSeats <= 0 and tripInfo.Participant_Num >= tripInfo.Participant_Cap:
                # The person has zero newSeats and tries to join a trip with maximum/over maximum people
                return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, errorMessage="Due to the current size of this trip, you must be a driver with at least one car capacity to join.")
            Participants.query.addParticipant(tempUser, isDriver, newSeats, int(FormKey), False, False)
            flash('New entry was successfully posted')
            return "Successful"
            # return redirect(url_for('main.tripPage', TripKey=str(FormKey)))
#
# @api_bp.route('/editParticipant/<FormKey>', methods=['POST', 'GET'])
# @login_required
# def editParticipant(FormKey):
#     tripInfo = Master.query.filter_by(id=FormKey).first()
#     you = Participants.query.filter_by(accountID=flask.session['Googledata']['id'], Master_Key=FormKey).first()
#     form = EditTripMemberPOA(Driver_Box=you.Driver, CarCapacity_Box=str(you.Car_Capacity), PotentialLeader_Box=you.OpenLeader)
#     if request.method == 'GET':
#         # return redirect(url_for('main.tripPage', TripKey=str(FormKey), autoModal="#"))
#         return render_template('EditTripMemberModal.html', form=form, tripInfo=tripInfo)
#     if request.method == 'POST':
#         if form.validate() == False:
#             flash('All fields are required.')
#             # print("terrible things are afoot")
#             # print(render_template('EditTripMemberModal.html', form=form, tripInfo=tripInfo, errorMessage=""))
#             # print("Below is the redirect")
#             # print(redirect(url_for('main.tripPage', TripKey=str(FormKey), autoModal="#")))
#             # return redirect(url_for('main.tripPage', TripKey=str(FormKey), autoModal="editParticipant"))
#             return render_template('EditTripMemberModal.html', form=form, tripInfo=tripInfo)
#         else:
#             newSeats = int(form.data["CarCapacity_Box"][:])
#             isDriver = form.data["Driver_Box"]
#             # Makes the number of seats and driver status consistent.
#             if form.data["Driver_Box"] == False:
#                 newSeats = 0
#             if newSeats == 0:
#                 isDriver = False
#             # Congratulations! You submitted your form and all fields were filled out properly.
#             you.editParticipantInfo(isDriver, newSeats, form.data["PotentialLeader_Box"])
#             db.session.commit()
#             print("things worked!")
#             return "Successful"
#             # return redirect(url_for('main.tripPage', TripKey=str(FormKey), autoModal="#"))
#
# @api_bp.route('/checkAddParticipant/<FormKey>', methods=['POST', 'GET'])
# @login_required
# def checkAddParticipant(FormKey):
#     """
#     Checks to see whether a new participant can fit in a trip.
#     :param FormKey:
#     :return:
#     """
#     print("You shouldn't even be here!")
#     # This whole thing is dead code.
#     tempTrip = Master.query.filter_by(id=FormKey).first()
#     tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
#     if tempTrip.Participant_Cap < tempTrip.Participant_Num + 1 and tempTrip.Car_Cap < tempTrip.Car_Num + 1:
#         # You cannot join the trip, no buts about it.
#         # TODO: FLASH A THING ON THE SCREEN
#         return redirect(url_for("main.tripPage", FormKey=str(FormKey)))
#     else:
#         # You can join, no problem!
#         return redirect(url_for("main.addParticipant", FormKey=str(FormKey)))
#
#
# @api_bp.route('/tripDisplay')
# @login_required
# def tripDisplay():
#     listOfParticipants = Participants.query.filter_by(accountID=flask.session['Googledata']['id']).all()
#     listOfTrips = []
#     for those in listOfParticipants:
#         listOfTrips.append(Master.query.filter_by(id=those.Master_Key).first())
#     return render_template('DisplayTripsModal.html', listOfTrips=listOfTrips)
#
# @api_bp.route('/cannotLeave')
# def cannotLeave():
#     return render_template('DisplayMessageModal.html', message="You are this trip's coordinator. You cannot leave until you have passed the role onto someone else.", title="Cannot Leave Trip")
#
#
# @api_bp.route('/deleteParticipant/<personID>/<tripID>')
# def removeParticipant(personID, tripID):
#     # Beware possible nefarious individuals typing in this URL to remove others from a trip.
#     Participants.query.removeParticipant(personID, tripID)
#     return redirect(url_for('main.tripPage', TripKey=tripID))
#
#
# @api_bp.route('/swapCoordinators/<oldLeaderID>/<newLeaderID>/<tripID>')
# def swapCoordinators(oldLeaderID, newLeaderID, tripID):
#     Participants.query.swapCordinator(oldLeaderID, newLeaderID, tripID)
#     return redirect(url_for('main.tripPage', TripKey=tripID))
#
# #UPPERBOUND
# @api_bp.route("/send")
# def index():
#     # msg = mail.send_message("Hello", sender="pzgearcloset@gmail.com", recipients=["mvonallm@students.pitzer.edu"])
#     msg = Message(subject="Hello", body="Hey there man what's up.", sender="pzgearcloset@gmail.com", recipients=["mvonallm@students.pitzer.edu"])
#     mail.send(msg)
#     return "sent"
# #LOWERBOUND
#
# @api_bp.route("/getUsers")
# def getUsers():
#     userList = Account.query.all()
#     return jsonify(data=[i.serializeUser for i in userList])
#
# @api_bp.route("/getTrips")
# def getTrips():
#     tripList = Master.query.all()
#     return jsonify(data=[i.serializeTrip for i in tripList])
#
# @api_bp.route("/makeAdmin/<userNum>")
# @login_required
# @admin_required
# def makeAdmin(userNum):
#     # userNum is the Account's ID number, not the googleNum.
#     tempUser = Account.query.filter_by(id=int(userNum)).first()
#     tempUser.admin = 1
#     db.session.commit()
#     return jsonify(status="success")
#
# @api_bp.route('/addParticipant/<FormKey>/<userNum>', methods=['POST', 'GET'])
# @login_required
# @admin_required
# def adminAddParticipant(FormKey, userNum):
#     """
#     Adds a participant to a trip.
#     :param FormKey:
#     :param userNum:
#     :return:
#     """
#     tempUser = Account.query.filter_by(id=userNum).first()
#     tripInfo = Master.query.filter_by(id=FormKey).first()
#     form = AddToTripPOA(Driver=False, Car_Capacity=str(tempUser.carCapacity))
#     if request.method == 'GET':
#         return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, errorMessage="")
#     if request.method == 'POST':
#         if form.validate() == False:
#             flash('All fields are required.')
#             return render_template('AddToTripModal.html', form=form, tripInfo=tripInfo, errorMessage="")
#         else:
#             # Right now admins can force-add people, even if a trip is full on either cars OR people.
#             # You might want to make some edge cases in the trip code to handle these possible exceptions elegantly/
#             newSeats = int(form.data["Car_Capacity"][:])
#             isDriver = form.data["Driver"]
#             # Makes the number of seats and driver status consistent.
#             if form.data["Driver"] == False:
#                 newSeats = 0
#             if newSeats == 0:
#                 isDriver = False
#             Participants.query.addParticipant(tempUser, isDriver, newSeats, int(FormKey), False, False)
#             flash('New entry was successfully posted')
#             return "Successful"
#
# @api_bp.route("/deleteTrip/<tripID>")
# @login_required
# def deleteTrip(tripID):
#     tempUser = Account.query.filter_by(googleNum=flask.session['Googledata']['id']).first()
#     tempTrip = Master.query.filter_by(id=tripID).first()
#     tempParticipants = Participants.query.filter_by(Master_Key=tripID).first()
#     if tempUser.admin == 1 or tempUser.admin == 2 or (tempTrip.Participant_Num == 1 and tempParticipants.accountID == flask.session['Googledata']['id']):
#         # Check to see if either the user has the admin privileges to delete a trip,
#         # or that they are the last person on a trip when it is deleted.
#         # tempTrip.delete() destroys participants too. (90% sure)
#         db.session.delete(tempTrip)
#         db.session.commit()
#         return jsonify(status="success")
#     else:
#         return render_template('DisplayMessageModal.html',
#                                message="You are not the last person on this trip. You must have admin privileges to perform this action.",
#                                title="Cannot Delete Trip")
#
# @api_bp.route("/freezeTrip/<tripID>")
# @login_required
# @admin_required
# def freezeTrip(tripID):
#     tempTrip = Master.query.filter_by(id=tripID).first()
#     tempTrip.Frozen = True
#     db.session.commit()
#     return jsonify(status="success")
#
# @api_bp.route("/thawTrip/<tripID>")
# @login_required
# @admin_required
# def thawTrip(tripID):
#     tempTrip = Master.query.filter_by(id=tripID).first()
#     tempTrip.Frozen = False
#     db.session.commit()
#     return jsonify(status="success")
#
# @api_bp.route("/adminDialogueUser/<userID>")
# @login_required
# @admin_required
# def adminDialogueUser(userID):
#     # tempParticipants = Participants.query.filter_by(id=userID).all()
#     # tempTrips = []
#     # for people in tempParticipants:
#     #     tempTrips.append(people.Master_Key)
#     ourAccount = Account.query.filter_by(id=userID).first()
#     trips = Master.query.all()
#     tempTwins = {}
#     coupledTrips = []
#     # print(Participants.query.all())
#     for item in trips:
#         tempTwins["trip"] = item
#         # print("ID: " + str(item.id))
#         # print(Participants.query.filter_by(id=userID, Master_Key=item.id).first())
#         # print(bool(Participants.query.filter_by(id=userID, Master_Key=item.id).first() is not None))
#         ourParticipant = Participants.query.filter_by(accountID=ourAccount.googleNum, Master_Key=item.id).first()
#         # print(ourParticipant)
#         tempTwins["onTheTrip"] = bool(ourParticipant is not None)
#         # print(tempTwins["onTheTrip"])
#         if tempTwins["onTheTrip"]:
#             tempTwins["numSeats"] = ourParticipant.Car_Capacity
#         else:
#             tempTwins["numSeats"] = 0
#         coupledTrips.append(copy.deepcopy(tempTwins))
#     #print(coupledTrips)
#     return render_template("AdminDialogueUserModal.html", trips=coupledTrips, userID=userID, isAdmin=ourAccount.admin)
#
# @api_bp.route("/adminDialogueTrip/<tripID>", methods=['POST', 'GET'])
# @login_required
# @admin_required
# def adminDialogueTrip(tripID):
#     # Hello world.
#     # Received a JSON, which becoemes a dictionary. Has keys in it telling whether we want to delete this
#     # trip, to freeze this trip, how long we want to freeze it for, and how to change max cars,
#     # max participants, and whether the trip is substance-free.
#     if request.method == 'GET':
#         master = Master.query.filter_by(id=tripID).first()
#         trip = Trips.query.filter_by(id=tripID).first()
#         return render_template("AdminDialogueTripModal.html", trip=trip, master=master)
#     elif request.method == 'POST':
#         return "Success! Neato."
#
# @api_bp.route("/updateUserAccount", methods=['POST', 'GET'])
# @login_required
# def updateUserAccount():
#     response = request.get_json(force=True)
#     print(response)
#     user = Account.query.filter_by(googleNum=response["googleNum"]).first()
#     error = Account.query.updateAccount(response, user) # updates account and checks for type errors
#     db.session.commit()
#     if error:
#         return jsonify(status="error", user=Account.query.filter_by(googleNum=response["googleNum"]).first().accessData(), errors=error)
#     else:
#         return jsonify(status="success", user=Account.query.filter_by(googleNum=response["googleNum"]).first().accessData(), errors={})
#
#
# @api_bp.route("/updateUser", methods=['POST', 'GET'])
# @login_required
# @admin_required
# def updateUser():
#     response = request.get_json(force=True)
#     print(response)
#     for item in response["tripsOut"]:
#         Master.query.updateUser(item, response["adminOut"])
#     # print(response)
#     return jsonify(result="success")
#
# @api_bp.route("/updateTrip", methods=['POST', 'GET'])
# @login_required
# @admin_required
# def updateTrip():
#     response = request.get_json(force=True)
#     print(response)
#     # print("sick memes, bro")
#     # Write a custom query to update this particular trip with these new values.
#     # Then return success.
#     Master.query.updateTrip(response)
#     #
#     # for item in response["tripsOut"]:
#         # Master.query.updateUser(item, response["adminOut"])
#     # print(response)
#     return jsonify(result="success")
