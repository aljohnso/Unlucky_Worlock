from flask_sqlalchemy import SQLAlchemy, inspect
from DatabaseConnection.DatabaseQuery import POA_db_query
from DatabaseConnection.DatabaseSubmissionConstructors import MasterConstructor, TripConstructor, ParticipantConstructor
db = SQLAlchemy()
# this tells SQLAlchemy to add our custom query class DBconnection

class Master(db.Model):
    """
        Contains Schema for master contains basic trip info
    """
    __tablename__ = "Master"
    query_class = POA_db_query
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


    Trip_Participants = db.relationship('Participants', backref = "Master", lazy='dynamic', cascade="all,delete")
    Trip_Trip = db.relationship('Trips', backref="Master", lazy='dynamic', cascade="all,delete")

    def __init__(self, form):
        MasterDict = MasterConstructor(form).master
        self.Trip_Name = MasterDict['Trip_Name']
        self.Departure_Date = MasterDict['Departure_Date']
        self.Return_Date = MasterDict['Return_Date']
        self.Details_Short = MasterDict['Details']  # name changes here
        self.Post_Time = MasterDict['Post_Time']
        self.Participant_num = MasterDict['Participant_num']
        self.Participant_cap = MasterDict['Car_Capacity']  # name changes here
        self.Trip_Location = MasterDict['Trip_Location']
        self.Car_Num = MasterDict['Car_Num']
        self.Car_Cap = MasterDict['Car_Cap']
        assert inspect(Master).primary_key[0] is not None  # this may not do anything

    def __repr__(self):
        return '<Trip %r> ' + str(self.Trip_Name) + str(self.Details_Short)


class Trips(db.Model):
    """
        Schema for the trips table contains detailed info for trips
    """
    __tablename__ = "Trips"
    query_class = POA_db_query
    id = db.Column(db.Integer, primary_key=True)
    Master_Key = db.Column(db.Integer, db.ForeignKey("Master.id",
                                                     ondelete="CASCADE"))
    Master_Relationship = db.relationship("Master", backref=db.backref("Trips", cascade="all,delete"))

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
        self.Additional_Costs = TripDict['Additional_Cost']#Name changes
        self.Total_Cost = TripDict["Total_Cost"]
        self.Cost_BreakDown = TripDict['Cost_Breakdown']#name Changes
        self.Substance_Free = TripDict["Substance_Free"]
        self.Weather_Forecast = TripDict["Weather_Forcast"]#name change
        self.Master_Key = TripDict['Master_Key']
        assert self.Master_Key is not None
        assert self.Master_Key is Masterid

    def __repr__(self):
        return '<Trips %r>' % self.Master_Key


class Participants(db.Model):
    __tablename__ = "Participants"
    query_class = POA_db_query
    id = db.Column(db.Integer, primary_key=True)
    Master_Key = db.Column(db.Integer, db.ForeignKey("Master.id",
                                                     ondelete="CASCADE"))
    Master_Relationship = db.relationship("Master", backref=db.backref("Participants", cascade="all,delete"))
    Participant = db.Column(db.String(120))
    Phone = db.Column(db.Integer)
    Email = db.Column(db.String(120))
    Driver = db.Column(db.Integer)
    Car_Capacity = db.Column(db.Integer)

    def __init__(self, form, Masterid):
        ParticpantDict = ParticipantConstructor(form, Masterid).participant
        self.Participant = ParticpantDict['Participant']
        self.Phone = ParticpantDict['Phone']
        self.Email = ParticpantDict['Email']
        self.Driver = ParticpantDict['Driver']
        self.Car_Capacity = ParticpantDict['Car_Capacity']
        self.Master_Key = ParticpantDict["Master_Key"]
        assert self.Master_Key is not None
        assert self.Master_Key is Masterid

    def __repr__(self):
        return '<Particpant %r>' % self.Participant

class TripModel():
    """
    This class is a work around for the fact we need master id to create the other to parts of the trip
    It makes me wounder if having trip and master seperate was a good idea but it is forced anyway by particpant

    NOTE: This will only work if called when the database is in an application context without the proper context
    we should get some wacky error message saying as much
    """
    def __init__(self, form):
        master = Master(form)
        db.session.add(master)
        db.session.flush()
        db.session.refresh(master)
        self.master = master
        self.trip = Trips(form, master.id)
        self.leader = Participants(form, master.id)
        assert self.master is not None
        assert self.trip is not None
        assert self.leader is not None

    def addModel(self):
        """
        Will add trip to db after construction
        NOTE: Will need to commit after this method
        is called to insure that it is added to the db
        """
        db.session.add(self.trip)
        db.session.add(self.leader)
        # db.session.add(self.master)


