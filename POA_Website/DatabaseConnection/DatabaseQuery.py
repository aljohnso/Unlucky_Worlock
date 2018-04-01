import datetime, re

from flask_sqlalchemy import BaseQuery

from DatabaseConnection import DataBaseSchema as Schema


class Master_db_query(BaseQuery):

    def checkTrip(self, server_time = datetime.date.today()):
        """
        :param server_time: the current date can be changed for testing purposes
        :return: a list of Master objects that contain all trips that are going out
        in the futre while the past ones have been deleted
        """
        # Get all expired trips.
        allTrips = Schema.Master.query.all()
        #server_time = datetime.datetime.now()  <-- Old code
        expiredTrips = Schema.Master.query.filter(Schema.Master.Departure_Date <= server_time - datetime.timedelta(days=1)).all()
        print("Trip Cutoff Time:")
        print(server_time - datetime.timedelta(days=1))
        for trip in allTrips:
            print("Trip Info:")
            print(trip.Departure_Date <= server_time - datetime.timedelta(days=1))
            print(trip.Departure_Date)
        print("Expired trips:")
        print(expiredTrips)
        for trip in expiredTrips:
            # Delete every trip and their children.
            Schema.db.session.delete(trip)
        # Commit changes.
        Schema.db.session.commit()
        return Schema.Master.query.all()
    def updateUser(self, update, isAdminNow):
        """
        Update the Participant attached to an Account.
        (Is meant to be called in a for loop, using a different "update" input each time)
        :param update: A dictionary containing vital information for updating a participant.
        :param isAdminNow: A Boolean telling whether this person should be made into an admin.
        :return: Void.
        """
        #print(update)
        # Retrieve both the Account and Participant for this update.
        ourAccount = Schema.Account.query.filter_by(id=int(update["userID"])).first()
        ourParticipant = Schema.Participants.query.filter_by(Master_Key=update["tripID"], accountID=ourAccount.googleNum).first()
        if bool(update["add"]):
            if ourParticipant is None:
                # Add a participant if there currently isn't one and we want there to be one.
                Schema.Participants.query.addParticipant(tempUser=ourAccount, isDriver=(int(update["carCapacity"]) > 0), carSeats=int(update["carCapacity"]), masterID=update["tripID"])
            else:
                # Make updates to this participant.
                if int(update["carCapacity"]) > 0:
                    # Participant is a driver.
                    ourParticipant.Driver = True
                    ourParticipant.Car_Capacity = int(update["carCapacity"])
                else:
                    # Participant is not a driver.
                    ourParticipant.Driver = False
                    ourParticipant.Car_Capacity = 0
                # Find the desired Master.
                tempMaster = Schema.Master.query.filter_by(id=update["tripID"]).first()
                if tempMaster is None:
                    # No such Master exists! What have you done?
                    print("AAAAAAHHH THERE IS NO SUCH TRIP!")
                # Re-compute the car capacity and number of participants on the trip after these updates are completed.
                driverList = Schema.Participants.query.filter_by(Master_Key=update["tripID"], Driver=True).all()
                tempMaster.Car_Num = len(driverList)
                sumCapacity = 0
                for people in driverList:
                    sumCapacity += people.Car_Capacity
                tempMaster.Participant_Cap = sumCapacity
            if update["isCoordinator"]:
                # Make this participant into a coordinator!
                # Find the previous coordinator for the trip.
                previousCoordinator = Schema.Participants.query.filter_by(Leader=True, Master_Key=update["tripID"]).first()
                if previousCoordinator is not None:
                    # Make the previous coordinator, if they exist, not the coordinator anymore.
                    previousCoordinator.Leader = False
                # Make this participant into the new coordinator.
                ourParticipant.Leader = True
        else:
            if ourParticipant is not None:
                # Remove this participant if they do exist, we want to get rid of them.
                Schema.Participants.query.removeParticipant(personID=ourAccount.googleNum, tripID=update["tripID"])
        # Update admin status.
        #TODO: Make this into its own query for stylistic purposes, is currently being called a number of times equal to how many trips we have!
        if isAdminNow:
            ourAccount.admin = 1
        else:
            ourAccount.admin = 0
        Schema.db.session.commit()
    def updateTrip(self, form):
        print("All data:")
        print(form)
        thisTrip = Schema.Trips.query.filter_by(id=form["id"]).first();
        thisMaster = Schema.Master.query.filter_by(id=form["id"]).first();
        print(thisTrip)
        print(thisMaster)
        if form["substancefree"] == True:
            thisTrip.Substance_Free = 1
        else:
            thisTrip.Substance_Free = 0
        thisMaster.Frozen = form["frozen"]
        thisMaster.timeTillUnfreeze = int(form["thawtime"])
        # Here is the broken part! It updates participant cap directly!
        # Will be overridden in the future by changes to car capacities!
        thisMaster.Participant_Cap = int(form["maxparticipants"])
        thisMaster.Car_Cap = int(form["maxcars"])
        Schema.db.session.commit()



class Participant_manipulation_query(BaseQuery):
    def addParticipant(self, tempUser, isDriver, carSeats, masterID):
        """
        Adds a new participant to the database. We make them a leader if they're the first participant on a trip.
        """
        isLeader = False
        isOpenLeader = False
        print("You were added.")
        # TODO: THE BELOW TODO IS REALLY IMPORTANT, because you have so many stupid arguments in this function that
        # TODO: cont. ... COULD BE BETTER ADDRESSED IN CONTROLLERS' addParticipant!!!
        # TODO: Write a function to do all this stuff in the else case that uses the decorated login protector.
        if Schema.Participants.query.filter_by(Master_Key=masterID, Leader=True).first() is None:
            isLeader = True
        participant = Schema.Participants(tempUser, isDriver, carSeats, masterID, isLeader, isOpenLeader)
        Schema.db.session.add(participant)
        Schema.db.session.commit()
        master = Schema.Master.query.filter_by(id=masterID).first()
        master.Participant_Num = len(Schema.Participants.query.filter_by(Master_Key=masterID).all())
        driverList = Schema.Participants.query.filter_by(Master_Key=masterID, Driver=True).all()
        master.Car_Num = len(driverList)
        sumCapacity = 0
        for people in driverList:
            sumCapacity += people.Car_Capacity
        master.Participant_Cap = sumCapacity
        Schema.db.session.commit()
        # NOTDOINGTHIS: If they don't have a car, redirect them to the tripPage without running them through the form asking if they want to be a driver.
        # FINISHED: Check to make sure no data is being asked of the user that we can easily get from their profile info.
        # TODO: Incorporate allergies and stuff into the addition of new participants, and have it display on the main page.

    def removeParticipant(self, personID, tripID):
        """
        Locate a participant attached to a specific Account on a specific trip, and remove them from existence.
        Modify the variables for their trip to remain consistent in their absence.
        :param personID: This is the googleNum of the Account attached to this new participant.
        :param tripID: The id of the Master for this Participant.
        :return: Void.
        """
        # Find the participant we're looking for (in terms of the database, not the Python object).
        tempParticipant = Schema.Participants.query.filter_by(accountID=personID, Master_Key=tripID)
        # Retrieve the participant themselves if they are a leader. Otherwise, this gives us a None object.
        leaderGone = tempParticipant.first().Leader
        # Find the Master that this participant is on.
        tempMaster = Schema.Master.query.filter_by(id=tripID).first()
        # Delete the participant.
        tempParticipant.delete()
        # Get the first person, if they exist, who didn't necessarily want to be the leader.
        otherParticipant = Schema.Participants.query.filter_by(Master_Key=tripID).first()
        # Get the first person, if they exist, who wanted to be the leader.
        nominatedLeader = Schema.Participants.query.filter_by(Master_Key=tripID, OpenLeader=True).first()
        if nominatedLeader is not None and leaderGone:
            # Made a nominated person the leader.
            nominatedLeader.Leader = True
        elif otherParticipant is not None and leaderGone:
            # Made a non-nominated person the leader.
            otherParticipant.Leader = True
        Schema.db.session.commit()
        # Reset statistics on the car capacity of this trip and the remaining number of participants.
        tempMaster.Participant_Num = len(Schema.Participants.query.filter_by(Master_Key=tripID).all())
        driverList = Schema.Participants.query.filter_by(Master_Key=tripID, Driver=True).all()
        tempMaster.Car_Num = len(driverList)
        sumCapacity = 0
        for people in driverList:
            sumCapacity += people.Car_Capacity
        tempMaster.Participant_Cap = sumCapacity
        Schema.db.session.commit()

    def swapCordinator(self, oldLeaderID, newLeaderID, tripID):
        """
        :param oldLeaderID: the current leader of the trip
        :param newLeaderID: someone who has concented to lead the trip
        :param tripID: the trip we are on
        :return: void only changes designations in the db
        """
        oldLeader = Schema.Participants.query.filter_by(accountID=oldLeaderID, Master_Key=tripID).first()
        newLeader = Schema.Participants.query.filter_by(accountID=newLeaderID, Master_Key=tripID).first()
        oldLeader.Leader = False
        oldLeader.OpenLeader = False
        newLeader.Leader = True
        newLeader.OpenLeader = False
        Schema.db.session.commit()



class Account_manipulation_query(BaseQuery):
    def createAccount(self, formData, session):
        """
        Make a new account.
        :param formData: 
        :param session: 
        :return: Void.
        """
        Schema.db.session.add(Schema.Account(formData, session))
        Schema.db.session.commit()

    def updateAccount(self, update, user):
        """
        Validate all inputs and place any errors we find into a dictionary.
        If that dictionary is empty, go ahead and update the account!
        Otherwise, return the dictionary with all of the encountered errors.
        :param update: 
        :param user: 
        :return: 
        """
        out = {}
        if not update['heightinput'].isdigit():
            out['heightinput'] = "Height must be an number in inches, no units"
        if not update['studentIDinput'].isdigit():
            out['studentIDinput'] = "Student ID must be a number"
        if not update["ageinput"].isdigit():
            out["ageinput"] = "Age must be a number"
        if not re.match("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", update['phoneNumerinput']):
            out['phoneNumerinput'] = "Phone number must be of form 000-000-0000"
        if not re.match("[^@]+@[^@]+\.[^@]+", update['emailinput']):
            out['emailinput'] = "We do not recognize this as a valid email address"
        if not out:
            #If the dictionary is still empty ie it has no errors then build the response object.
            user.height = update['heightinput']
            user.email = update['emailinput']
            user.studentIDNumber = update['studentIDinput']
            user.age = update["ageinput"]
            user.phoneNumber = update['phoneNumerinput']
            Schema.db.session.commit()
        return out
