import datetime

from DatabaseConnection import DataBaseSchema as Schema
from flask_sqlalchemy import BaseQuery

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
            Schema.db.session.commit()#comit changes

            return Schema.Master.query.all()

class Participant_manipulation_query(BaseQuery):
    def addParticipant(self, tempUser, isDriver, masterID):
        """
        stuff
        """
        # TODO: Write a function to do all this stuff in the else case that uses the decorated login protector.
        participant = Schema.Participants(tempUser, isDriver, masterID)
        Schema.db.session.add(participant)
        Schema.db.session.commit()
        master = Schema.Master.query.filter_by(id=masterID).first()
        master.Participant_num = len(Schema.Participants.query.filter_by(Master_Key=masterID).all())
        driverList = Schema.Participants.query.filter_by(Master_Key=masterID, Driver=True).all()
        master.Car_Num = len(driverList)
        sumCapacity = 0
        for people in driverList:
            sumCapacity += people.Car_Capacity
        master.Participant_Cap = sumCapacity
        Schema.db.session.commit()
        # TODO: If they don't have a car, redirect them to the TripPage without running them through the form asking if they want to be a driver.
        # TODO: Check to make sure no data is being asked of the user that we can easily get from their profile info.



# class DatabaseConnection1(db):
#
#
#     def deleteTrip(self, MasterID):
#         """
#             Will Delete trip from database based on trip ID from Master Table and Trips Table
#             :param TripID:
#             :return: None
#         """
#         print(MasterID)
#         Master.query.filter_by(id=MasterID).delete()
#         self.db.session.commit()
#

#
#
#     def Addparticipant(self, Form, MasterID):
#         """
#         :param Form: from participant
#         :param MasterID: ID of trip of to add to
#         :return: adds particpant to participant table
#         """
#         participant = ParticipantCommandConstructor(Form, MasterID).participant
#         participantObject = Participants(participant)
#         car_capacity = participantObject.Car_Capacity
#         print(participant)
#         print(car_capacity)
#         db.session.add(participantObject)
#         Master.Participant_num += 1
#         Master.Participant_cap += car_capacity
#         self.db.session.commit()
#
#     def getParticipants(self, masterID):
#         """
#         :param masterID: id of trip
#         :return: List of participant objects
#         """
#         try:
#
#             return Participants.query.filter_by(Master_Key = masterID)
#         except:
#             return None
#
#     def deleteParticpant(self, participant_id):
#         ParticipantToRemove = Participants.query.filter_by(id = participant_id)
#         Master.Participant_num -= 1#reduce num Particpants
#         Master.Participant_cap -= ParticipantToRemove.car_capacity#reduce spots on trip
#         ParticipantToRemove.delete()
#         self.db.session.commit()
#
#     def getTrip(self,Master_Key):
#         """
#         :param Master_Key: whichever trip you want
#         :return: info for trip Page
#         """
#         master_details = Master.query.filter_by(id = Master_Key)
#         trip_details = Trips.query.filter_by(Master_Key = Master_Key)
#         particpant_details = Participants.query.filter_by(Master_Key = Master_Key)
#         return trip_details, master_details, particpant_details
#
#     def checkParticipant(self, Form, tripID):
#         """
#         :param Form: The participant form from the forms package which is submited throught the addParticpant URL
#         :param tripID: The ID of the trip
#         :return: Bollean True means that trip driver cap reached, false means the oppisit du
#         This method will check to make sure that the trip has not reached car capacity
#         TODO: Create a class that handels trip states/ some way to cache states
#         """
#         drivers = self.cursor.execute('Select Driver from Participants Where Trips_Key=' + tripID).fetchall()
#         print(drivers)
#
#
#
#
#
