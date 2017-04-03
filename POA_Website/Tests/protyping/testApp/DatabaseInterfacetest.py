import sqlite3, datetime
from DatabaseConnection.DatabaseSubmissionConstructors import TripConstructor, MasterConstructor, ParticipantConstructor
from DatabaseConnection.DataBaseSchema import db, Master, Participants, Trips



class DatabaseTest:

    def __init__(self):
        self.db = db

    def addMaster(self, Form):
            data  = MasterConstructor(Form).master
            print(data)
            test = Master(data)
            print(test)
            db.session.add(test)
            db.session.commit()
            info = Master.query.all()
            print(info)
            return info


