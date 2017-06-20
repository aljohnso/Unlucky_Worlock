from flask_sqlalchemy import SQLAlchemy, inspect
from DatabaseConnection.DatabaseQuery import POA_db_query
from DatabaseConnection.DatabaseSubmissionConstructors import MasterConstructor, TripConstructor, ParticipantConstructor
import json
db = SQLAlchemy()
# this tells SQLAlchemy to add our custom query class DBconnection

class Master(db.Model):
    """
        Contains Schema for master contains basic trip info
    """
    __tablename__ = "Master"
    query_class = POA_db_query
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    Trip_Name = db.Column(db.String(100))
    Departure_Date = db.Column(db.Date)
    Return_Date = db.Column(db.Date)
    Details_Short = db.Column(db.String(100))
    Post_Time = db.Column(db.Date)
    Participant_num = db.Column(db.Integer)
    Participant_cap = db.Column(db.Integer)
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
    Phone = db.Column(db.String(120))
    Email = db.Column(db.String(120))
    Driver = db.Column(db.Boolean)
    Car_Capacity = db.Column(db.Integer)

    def __init__(self, account, driver , masterID):
        tempData = account.accessData()
        self.Participant = tempData["username"] #ParticipantDict['Participant']
        self.Phone = tempData["phoneNumber"] #ParticipantDict['Phone']
        self.Email = tempData["email"] #ParticipantDict['Email']
        self.Driver = driver #ParticipantDict['Driver']
        self.Car_Capacity = tempData["carCapacity"] #ParticipantDict['Car_Capacity']
        self.Master_Key = masterID
        assert self.Master_Key is not None
        #assert self.Master_Key is masterID

    def __repr__(self):
        return '<Participant %r>' % self.Participant

class TripModel():
    """
    This class is a work around for the fact we need master id to create the other to parts of the trip
    It makes me wounder if having trip and master separate was a good idea but it is forced anyway by particpant

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
        # self.leader = Participants(form, master.id)
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
        # db.session.add(self.leader)
        # db.session.add(self.master)  # not sure if this is needed

class Account(db.Model):
    # Defines a variable with certain fixed parameters, much like one would in C#.
    # Maybe look up a way to record how many objects are in your database?
    id = db.Column(db.String(80), primary_key=True)
    googleNum = db.Column(db.String(80))
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
    phoneNumber = db.Column(db.Integer)
    carCapacity = db.Column(db.Integer)
    locale = db.Column(db.String(80))
    # How to structure the profile picture? What data type, and how do I use it?
    # In total, there are 11 variables so far per account.

    def __init__(self, inputData):
        self.id = str(inputData['googleNum'][:])
        self.googleNum = str(inputData['googleNum'][:]) # Given
        self.picture = str(inputData['picture'][:])
        self.username = str(inputData['username'][:]) #username
        self.email = str(inputData['email'][:]) #email # Not given, surprisingly? Ask Alasdair about this.
        self.firstName = str(inputData['firstName'][:]) # Given
        self.lastName = str(inputData['lastName'][:]) # Given
        self.age = int(inputData['age'][:]) #age
        self.height = int(inputData['height'][:]) #height
        self.allergies = str(inputData['allergies'][:]) #allergies
        self.dietRestrictions = str(inputData['dietRestrictions'][:]) #dietRestrictions
        self.studentIDNumber = int(inputData['studentIDNumber'][:]) #studentIDNumber
        self.phoneNumber = str(self.formatPhoneNumber(inputData['phoneNumber'][:])) #phoneNumber
        self.carCapacity = int(inputData['carCapacity'][:]) #capCapacity
        self.locale = str(inputData['locale'][:])
        # Also given a picture. That's neat. How to access it?

    def __repr__(self):
        #return '<User %r, ID: >' % self.username
        return '<User ' + self.username + ', ID: ' + self.googleNum + '>'

    def formatPhoneNumber(self, oldNum):
        newNum = oldNum.replace("(", "")
        newNum = newNum.replace(")", "")
        newNum = newNum.replace("-", "")
        newNum = newNum.replace(" ", "")
        if len(newNum)==10:
            print(newNum[0:3] + "-" + newNum[3:6] + "-" + newNum[6:10])
            return newNum[0:3] + "-" + newNum[3:6] + "-" + newNum[6:10]
        else:
            print(oldNum)
            return oldNum

    def modifyAccount(self, rawData):
        data = json.loads(rawData)
        print('Insert a thing here! Produce a spreadsheet already filled with the users information, then have it resubmit to this function.')
        self.username = str(data['username'][:])  # username
        self.email = str(data['email'][:])  # email # Not given, surprisingly? Ask Alasdair about this.
        self.firstName = str(data['firstName'][:])  # Given
        self.lastName = str(data['lastName'][:])  # Given
        #self.gender = str(data['gender'][:])
        self.age = int(data['age'][:])  # age
        self.height = int(data['height'][:])  # height
        self.allergies = str(data['allergies'][:])  # allergies
        self.dietRestrictions = str(data['dietRestrictions'][:])  # dietRestrictions
        self.studentIDNumber = int(data['studentIDNumber'][:])  # studentIDNumber
        self.phoneNumber = str(self.formatPhoneNumber(data['phoneNumber'][:]))  # phoneNumber
        self.carCapacity = int(data['carCapacity'][:])  # capCapacity

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

def newUser(inputData):
    generatedUser = Account(inputData)
    return generatedUser

def createAccount(rawData):
    # Try making rawData a json file that you can then unpack. Test if it works? (future matthew -->)OR DON'T DO THAT
    #unpackedData = json.loads(rawData)
    #firstName = unpackedData['given_name'][:]
    #lastName = unpackedData['family_name'][:]
    #googleNum = unpackedData['id'][:]
    # WHY ARE WE NOT GIVEN THEIR EMAIL?
    # Have a variable that indicates how much security clearance they have; admin or user?
    # ^^^ Have three different levels: User, TechAdmin, and GearClosetWorker.  << from Alasdair
    #if os.path.exists(currentPath + '/' + databaseName):
    #    print('God is dead and WE HAVE KILLED HIM!')
    #else:
    #    with app.app_context():
    #        db.create_all()
    print('hi!')
    # Don't try to store different data types inside of the same database; it's totally not worth the trouble. Just work with Users.
    # If this works, how do we log into an account? Do we store a username and password in here?
    db.session.add(newUser(json.loads(rawData)))
    db.session.commit()
