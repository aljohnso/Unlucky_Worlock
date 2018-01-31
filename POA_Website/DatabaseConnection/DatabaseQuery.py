import datetime, re

from flask_sqlalchemy import BaseQuery

from DatabaseConnection import DataBaseSchema as Schema


class Master_db_query(BaseQuery):

    def checkTrip(self, server_time = datetime.datetime.now()):
            """
            :param server_time: the current date can be changed for testing puropuses
            :return: a list of Master objects that contain all trips that are going out
            in the futre while the past ones have been deleted
            """
            expiredTrips = Schema.Master.query.filter(Schema.Master.Departure_Date <= server_time)#get all
            for trip in expiredTrips:
                Schema.db.session.delete(trip)#delete every trip and there childeren
            Schema.db.session.commit()#commit changes
            return Schema.Master.query.all()
    def updateUser(self, update, isAdminNow):
        # ourTrip = Schema.Master.query.filter_by(id=update["tripID"]).first()
        print(update)
        ourAccount = Schema.Account.query.filter_by(id=int(update["userID"])).first()
        ourParticipant = Schema.Participants.query.filter_by(Master_Key=update["tripID"], accountID=ourAccount.googleNum).first()
        if bool(update["add"]):
            if ourParticipant is None:
                Schema.Participants.query.addParticipant(tempUser=ourAccount, isDriver=(int(update["carCapacity"]) > 0), carSeats=int(update["carCapacity"]), masterID=update["tripID"], isLeader=False, isOpenLeader=False)
            else:
                if int(update["carCapacity"]) > 0:
                    ourParticipant.Driver = True
                    ourParticipant.Car_Capacity = int(update["carCapacity"])
                else:
                    ourParticipant.Driver = False
                    ourParticipant.Car_Capacity = 0
        else:
            if ourParticipant is not None:
                Schema.Participants.query.removeParticipant(personID=ourAccount.googleNum, tripID=update["tripID"])
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
        thisMaster.Participant_Cap = int(form["maxparticipants"])
        thisMaster.Car_Cap = int(form["maxcars"])



class Participant_manipulation_query(BaseQuery):
    def addParticipant(self, tempUser, isDriver, carSeats, masterID, isLeader, isOpenLeader):
        """
        stuff
        """
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
        tempParticipant = Schema.Participants.query.filter_by(accountID=personID, Master_Key=tripID)
        leaderGone = tempParticipant.first().Leader
        #print(tempParticipant.first().Master_Key)
        # tripKey = tempParticipant.first().Master_Key
        tempMaster = Schema.Master.query.filter_by(id=tripID).first()
        tempParticipant.delete()
        # print("Person got deleted.")
        otherParticipant = Schema.Participants.query.filter_by(Master_Key=tripID).first()
        nominatedLeader = Schema.Participants.query.filter_by(Master_Key=tripID, OpenLeader=True).first()
        if nominatedLeader is not None and leaderGone:
            nominatedLeader.Leader = True
            # print("Made a nominated person the leader.")
        elif otherParticipant is not None and leaderGone:
            otherParticipant.Leader = True
            # print("Made a non-nominated person the leader.")
        Schema.db.session.commit()
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
        Schema.db.session.add(Schema.Account(formData, session))
        Schema.db.session.commit()

    def updateAccount(self, update, user):
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
            user.height = update['heightinput']
            user.email = update['emailinput']
            user.studentIDNumber = update['studentIDinput']
            user.age = update["ageinput"]
            user.phoneNumber = update['phoneNumerinput']
            Schema.db.session.commit()
        return out
