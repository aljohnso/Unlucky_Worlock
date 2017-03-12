import datetime
from DatabaseConnection.DatabaseSubmissionConstructors import TripConstructor, MasterConstructor, ParticipantConstructor
from DatabaseConnection import DataBaseSchema as Schema
from flask_sqlalchemy import BaseQuery

class POA_db_query(BaseQuery):

    def checkTrip(self, server_time = datetime.datetime.now()):
            """
            :param server_time: the current date can be changed for testing puropuses
            :return: a list of Master objects that contain all trips that are going out
            in the futre while the past ones have been deleted
            """
            Schema.Master.query.filter(Schema.Master.Post_Time <= server_time).delete()#get all
            Schema.db.session.commit()
            return Schema.Master.query.all()

  # def AddTrip(self, form):
  #     # add Master
  #     Masterinfo = MasterCommandConstructor(form)
  #     MasterObject = Master(Masterinfo.master)  # creates master object
  #     # print(Master)
  #     db.session.add(MasterObject)  # add master to db
  #     masterid = MasterObject.id
  #     print(masterid)
  #     # Add Trip
  #     Trip = TripCommandConstructor(form, masterid)
  #     TripInfo = Trip.trip
  #     TripObject = Trips(TripInfo)
  #     db.session.add(TripObject)
  #     # Add Leader
  #     LeaderObject = Participants(Trip.leader)  # leader is constructed when
  #     db.session.add(LeaderObject)
  #     db.session.commit()

#
# class DatabaseConnection1(db):
#     """
#         This class contains all maniputaltion fuctions for the database by intializing the object we open the database
#         Assumes POA Schema 12-26-16
#         TODO:CHANGE IF UPDATED
#
#     """
#
#     def __init__(self):
#         """
#             Will create Datbase Connection
#         """
#         # self.db = db #getting SQLAlchamey db from schema class
#
#     def AddTrip(self, form):
#         """'
#             used to construct the db insert for the trip table
#             :param form is the form from POAForms class  MakeTripFormPOA
#             :return: List of info for table
#         """
#         print("In add Trip")
#         #add Master
#         Masterinfo = MasterCommandConstructor(form)
#         MasterObject = Master(Masterinfo.master)#creates master object
#         # print(Master)
#         db.session.add(MasterObject)#add master to db
#         masterid = MasterObject.id
#         print(masterid)
#         #Add Trip
#         Trip = TripCommandConstructor(form,masterid)
#         TripInfo = Trip.trip
#         TripObject = Trips(TripInfo)
#         db.session.add(TripObject)
#         #Add Leader
#         LeaderObject = Participants(Trip.leader)#leader is constructed when
#         db.session.add(LeaderObject)
#         db.session.commit()
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
#     def checkTrip(self, server_time = datetime.datetime.now()):
#         """
#         :param server_time: the current date can be changed for testing puropuses
#         :return: a list of Master objects that contain all trips that are going out
#         in the futre while the past ones have been deleted
#         """
#         Master.query.filter_by(Master.Post_Time<server_time).delete()#get all
#         self.db.session.commit()
#         return Master.query.all()
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
