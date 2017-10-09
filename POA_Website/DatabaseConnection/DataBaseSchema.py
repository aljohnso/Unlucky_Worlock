from flask_sqlalchemy import SQLAlchemy, inspect

from DatabaseConnection.DatabaseQuery import Master_db_query, Participant_manipulation_query, Account_manipulation_query
from DatabaseConnection.DatabaseSubmissionConstructors import MasterConstructor, TripConstructor

db = SQLAlchemy()
# this tells SQLAlchemy to add our custom query class DBconnection

class Master(db.Model):
    """
    Contains Schema for master contains basic trip info
    """
    __tablename__ = "Master"
    query_class = Master_db_query
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    Trip_Name = db.Column(db.String(100))
    Departure_Date = db.Column(db.Date)
    Return_Date = db.Column(db.Date)
    Details_Short = db.Column(db.String(100))
    Post_Time = db.Column(db.Date)
    Participant_Num = db.Column(db.Integer)
    Participant_Cap = db.Column(db.Integer)
    Car_Num = db.Column(db.Integer)
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
        self.Participant_Num = MasterDict['Participant_num']
        self.Participant_Cap = 0 #Used to be this --> user.carCapacity  # name changes here
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
    query_class = Master_db_query
    id = db.Column(db.Integer, primary_key=True)
    Master_Key = db.Column(db.Integer, db.ForeignKey("Master.id", ondelete="CASCADE"))
    Master_Relationship = db.relationship("Master", backref=db.backref("Trips", cascade="all,delete"))

    Details = db.Column(db.String(3000))
    #Coordinator_Name = db.Column(db.String(70))
    #Coordinator_Email = db.Column(db.String(120))
    #Coordinator_Phone = db.Column(db.String(80))
    Gear_List = db.Column(db.String(3000))
    Trip_Meeting_Place = db.Column(db.String(120))
    Additional_Costs = db.Column(db.Integer)
    Total_Cost = db.Column(db.Integer)
    Cost_BreakDown = db.Column(db.String(3000))
    Substance_Free = db.Column(db.Integer)
    Weather_Forecast = db.Column(db.String(30000)) # Definitely not an optimal way of doing this.

    def __init__(self, form, Masterid):
        TripDict = TripConstructor(form, Masterid).trip
        #tempData = user.accessData()
        self.Details = TripDict['Details']
        #self.Coordinator_Name = tempData["username"]
        #self.Coordinator_Email = tempData["email"]
        #self.Coordinator_Phone = tempData["phoneNumber"]
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
    query_class = Participant_manipulation_query
    id = db.Column(db.Integer, unique=True, primary_key=True)
    accountID = db.Column(db.String(80))
    Master_Key = db.Column(db.Integer, db.ForeignKey("Master.id", ondelete="CASCADE"))
    Master_Relationship = db.relationship("Master", backref=db.backref("Participants", cascade="all,delete"))
    Participant = db.Column(db.String(120))
    Email = db.Column(db.String(120))
    Phone = db.Column(db.String(120))
    Driver = db.Column(db.Boolean)
    Leader = db.Column(db.Boolean)
    OpenLeader = db.Column(db.Boolean)
    Car_Capacity = db.Column(db.Integer)

    def __init__(self, account, driver, carSeats, masterID, leader, openCoordinator):
        tempData = account.accessData()
        self.accountID = tempData["googleNum"][:]
        self.Participant = tempData["username"][:] #ParticipantDict['Participant']
        self.Email = tempData["email"][:] #ParticipantDict['Email']
        self.Phone = tempData["phoneNumber"][:] #ParticipantDict['Phone']
        self.Driver = driver #ParticipantDict['Driver']
        self.Leader = leader
        self.OpenLeader = openCoordinator
        self.Car_Capacity = carSeats #ParticipantDict['Car_Capacity']
        self.Master_Key = masterID
        assert self.Master_Key is not None
        #assert self.Master_Key is masterID

    def __repr__(self):
        return '<Participant %r>' % self.Participant

    def changeUserInfo(self, user):
        self.Participant = user.username[:]
        self.Email = user.email[:]
        self.Phone = user.phoneNumber[:]

    def editParticipantInfo(self, isDriver, carSeats, openCoordinator):
        self.Driver = isDriver
        self.Car_Capacity = carSeats
        self.OpenLeader = openCoordinator
        master = Master.query.filter_by(id=self.Master_Key).first()
        driverList = Participants.query.filter_by(Master_Key=self.Master_Key, Driver=True).all()
        master.Car_Num = len(driverList)
        sumCapacity = 0
        for people in driverList:
            sumCapacity += people.Car_Capacity
        master.Participant_Cap = sumCapacity

class TripModel():
    """
    This class is a work around for the fact we need master id to create the other to parts of the trip
    It makes me wounder if having trip and master separate was a good idea but it is forced anyway by participant

    NOTE: This will only work if called when the database is in an application context without the proper context
    we should get some wacky error message saying as much
    """
    def __init__(self, formData, user):
        master = Master(formData)
        db.session.add(master)
        db.session.flush()
        db.session.refresh(master)
        self.master = master
        self.trip = Trips(formData, master.id)
        #self.leader = Participants(user, formData["Driver"], carSeats, master.id)
        assert self.master is not None
        assert self.trip is not None
        # assert self.leader is not None

    def addModel(self):
        """
        Will add trip to db after construction
        NOTE: Will need to commit after this method
        is called to insure that it is added to the db
        """
        db.session.add(self.trip)
        #db.session.add(self.leader)
        # db.session.add(self.master)  # not sure if this is needed


class Account(db.Model):
    query_class = Account_manipulation_query
    # Defines a variable with certain fixed parameters, much like one would in C#.
    # Maybe look up a way to record how many objects are in your database?
    id = db.Column(db.Integer, primary_key=True)
    googleNum = db.Column(db.String(80), unique=True)
    picture = db.Column(db.String(200))
    #newVar = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80)) #, unique=True)
    email = db.Column(db.String(120), unique=True)
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    #gender = db.Column(db.String(80))
    age = db.Column(db.String(80))
    # vvv Is this a thing? db.Double? Cuz I honestly don't know.
    height = db.Column(db.Integer)
    #height = db.Column(db.Float)
    # vvv Maybe represent these two (allergies and diet) as lists that you can add new elements to? Is that possible in SQL?
    # ^^^ Should be! Or maybe use a JSon file(?) which is apparently the same thing but for databases?
    allergies = db.Column(db.String(120))
    dietRestrictions = db.Column(db.String(120))
    studentIDNumber = db.Column(db.Integer)
    phoneNumber = db.Column(db.String(80))
    carCapacity = db.Column(db.Integer)
    locale = db.Column(db.String(80))
    # How to structure the h picture? What data type, and how do I use it?
    # In total, there are 11 variables so far per account.

    def __init__(self, formData, session):
        self.googleNum = str(session['Googledata']['id'][:]) # Given
        self.picture = str(session['Googledata']['picture'][:])
        self.username = str(formData['FirstName_Box'][:] + ' ' + formData['LastName_Box'][:]) #username
        self.email = str( formData['Email_Box'][:]) #email # Not given, surprisingly? Ask Alasdair about this.
        self.firstName = str(formData['FirstName_Box'][:]) # Given
        self.lastName = str(formData['LastName_Box'][:]) # Given
        self.age = int(formData['Age_Box']) #age
        self.height = int(formData['Height_Box']) #height
        self.allergies = str("TBD") #allergies
        self.dietRestrictions = str("TBD") #dietRestrictions
        self.studentIDNumber = int(formData['StudentIDNumber_Box']) #studentIDNumber
        self.phoneNumber = str(self.formatPhoneNumber(formData['PhoneNumber_Box'])) #phoneNumber
        self.carCapacity = int(formData['CarCapacity_Box']) #capCapacity
        self.locale = str(session['Googledata']['locale'])

    def __repr__(self):
        #return '<User %r, ID: >' % self.username
        return '<User ' + self.username + ', ID: ' + self.googleNum + '>'

    def formatPhoneNumber(self, oldNum):
        newNum = oldNum.replace("(", "")
        newNum = newNum.replace(")", "")
        newNum = newNum.replace("-", "")
        newNum = newNum.replace(" ", "")
        if len(newNum)==10:
            #print(newNum[0:3] + "-" + newNum[3:6] + "-" + newNum[6:10])
            return newNum[0:3] + "-" + newNum[3:6] + "-" + newNum[6:10]
        else:
            #print(oldNum)
            return oldNum

    def modifyAccount(self, formData, session):
        self.googleNum = str(session['Googledata']['id'][:])  # Given
        self.picture = str(session['Googledata']['picture'][:])
        self.username = str(formData['FirstName_Box'][:] + ' ' + formData['LastName_Box'][:])  # username
        self.email = str(formData['Email_Box'][:])  # email # Not given, surprisingly? Ask Alasdair about this.
        self.firstName = str(formData['FirstName_Box'][:])  # Given
        self.lastName = str(formData['LastName_Box'][:])  # Given
        self.age = int(formData['Age_Box'])  # age
        self.height = int(formData['Height_Box'])  # height
        self.allergies = str("TBD")  # allergies
        self.dietRestrictions = str("TBD")  # dietRestrictions
        self.studentIDNumber = int(formData['StudentIDNumber_Box'])  # studentIDNumber
        self.phoneNumber = str(self.formatPhoneNumber(formData['PhoneNumber_Box']))  # phoneNumber
        self.carCapacity = int(formData['CarCapacity_Box'])  # capCapacity
        self.locale = str(session['Googledata']['locale'])

    def accessData(self):
        dataDict = {
            'googleNum' : str(self.googleNum)[:],
            'picture' : str(self.picture)[:],
            'username' : str(self.username)[:],
            'email' : str(self.email)[:],
            'firstName': str(self.firstName)[:],
            'lastName': str(self.lastName)[:],
            'age': str(self.age)[:],
            'height': str(self.height)[:],
            'allergies': str(self.allergies)[:],
            'dietRestrictions': str(self.dietRestrictions)[:],
            'studentIDNumber': str(self.studentIDNumber)[:],
            'phoneNumber': str(self.phoneNumber)[:],
            'carCapacity': str(self.carCapacity)[:],
            'locale': str(self.locale)[:]
        }
        return dataDict


