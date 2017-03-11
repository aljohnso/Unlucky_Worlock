from flask_sqlalchemy import SQLAlchemy
from DatabaseConnection.DatabaseConnection import DatabaseConnection
from DatabaseConnection.DatabaseSubmissionConstructors import MasterConstructor, TripConstructor, ParticipantConstructor
db = SQLAlchemy()
# this tells SQLAlchemy to add our custom query class DBconnection

class Master(db.Model):
    """
        Contains Schema for master contains basic trip info
    """
    __tablename__ = "Master"
    query_class = DatabaseConnection
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    Trip_Name = db.Column(db.String(100))
    Departure_Date = db.Column(db.Date)
    Return_Date = db.Column(db.Date)
    Details_Short = db.Column(db.String(100))
    Post_Time = db.Column(db.Date)
    Participant_num = db.Column(db.Integer)
    Participant_cap = db.Column(db.Integer)
    Car_Num = db.column(db.Integer)
    Car_Cap = db.Column(db.Integer)
    Trip_Location = db.Column(db.String(100))
    Trip_Participants = db.relationship('Participants', backref = "Master", lazy='dynamic')
    Trip_Trip = db.relationship('Trips', backref="Master", lazy='dynamic')

    def __init__(self, form):
        MasterDict = MasterConstructor(form).master
        self.Trip_Name = MasterDict['Trip_Name']
        self.Departure_Date = MasterDict['Departure_Date']
        self.Return_Date = MasterDict['Return_Date']
        self.Details_Short = MasterDict['Details']
        self.Post_Time = MasterDict['Post_Time']
        self.Participant_num = MasterDict['Participant_num']
        self.Participant_cap = MasterDict['Car_Capacity']
        self.Trip_Location = MasterDict['Trip_Location']
        self.Car_Num = MasterDict['Car_Num']
        self.Car_Cap = MasterDict['Car_Cap']

    def __repr__(self):
        return '<Trip %r> ' + str(self.Trip_Name) + str(self.Details_Short)


class Trips(db.Model):
    """
        Schema for the trips table contains detailed info for trips
    """
    __tablename__ = "Trips"
    query_class = DatabaseConnection
    id = db.Column(db.Integer, primary_key=True)
    Master_Key = db.Column(db.Integer, db.ForeignKey("Master.id",
                                                     ondelete="CASCADE"), nullable=False)
    Details = db.Column(db.String(3000))
    Coordinator_Name = db.Column(db.String(70))
    Coordinator_Email = db.Column(db.String(120))
    Coordinator_Phone = db.Column(db.Integer)
    Gear_List = db.Column(db.String(3000))
    Trip_Meeting_Place = db.Column(db.String(120))
    Additional_Costs = db.Column(db.Integer)
    Total_Cost = db.Column(db.Integer)
    Cost_BreakDown = db.Column(db.String(3000))
    Substance_Free = db.Column(db.Integer)
    Weather_Forecast = db.Column(db.String(30000))#Def not an optimal way of doint this

    def __init__(self, form, Masterid):
        TripDict = TripConstructor(form, Masterid).trip
        self.Details = TripDict['Details']
        self.Coordinator_Name = TripDict['Coordinator_Name']
        self.Coordinator_Email = TripDict['Coordinator_Email']
        self.Coordinator_Phone = TripDict['Coordinator_Phone']
        self.Gear_List = TripDict['GearList']
        self.Trip_Meeting_Place = TripDict['Trip_Meeting_Place']
        self.Additional_Costs = TripDict['Additional_Cost']
        self.Total_Cost = TripDict["Total_Cost"]
        self.Cost_BreakDown = TripDict['Cost_Breakdown']
        self.Substance_Free = TripDict["Substance_Free"]
        self.Weather_Forecast = TripDict["Weather_Forcast"]
        self.Master_Key = TripDict['Master_Key']

    def __repr__(self):
        return '<Trips %r>' % self.Master_Key


class Participants(db.Model):
    __tablename__ = "Participants"
    query_class = DatabaseConnection
    id = db.Column(db.Integer, primary_key=True)
    Master_Key = db.Column(db.Integer, db.ForeignKey("Master.id",
                                                     ondelete="CASCADE"), nullable=False)
    Participant = db.Column(db.String(120))
    Phone = db.Column(db.Integer)
    Email = db.Column(db.String(120))
    Driver = db.Column(db.Integer)
    Car_Capacity = db.Column(db.Integer)

    def __init__(self, form, Masterid):
        ParticpantDict = ParticipantConstructor(form, Masterid).participant
        self.Participant = ParticpantDict['Participant']
        self.Phone = ParticpantDict['Email']
        self.Email = ParticpantDict['Phone']
        self.Driver = ParticpantDict['Driver']
        self.Car_Capacity = ParticpantDict['Car_Capacity']
        self.Master_Key = ParticpantDict["Master_Key"]

    def __repr__(self):
        return '<Particpant %r>' % self.Participant

class TripModel():
    """
    This class is a work around for the fact we need master id to create the other to parts of the trip
    It makes me wounder if having trip and master seperate was a good idea but it is forced anyway by particpant
    """
    def __init__(self, form):
        master = Master(form)
        self.master = master
        self.trip = Trips(form, master.id)
        self.leader = Participants(form, master.id)


