from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import json
app = Flask(__name__)

currentPath = 'C:/Users/matth_000/Downloads/DataBaseHolder'
databaseName = 'test.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getcwd() + '/test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/matth_000/Downloads/DataBaseHolder/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + currentPath + '/' + databaseName

db = SQLAlchemy(app)
# db.init_app(app)

class Account(db.Model):
    # Defines a variable with certain fixed parameters, much like one would in C#.
    # Maybe look up a way to record how many objects are in your database?
    id = db.Column(db.String(30), primary_key=True)
    googleNum = db.Column(db.String(30))
    picture = db.Column(db.String(200))
    #newVar = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80)) #, unique=True)
    email = db.Column(db.String(120), unique=True)
    firstName = db.Column(db.String(120))
    lastName = db.Column(db.String(120))
    age = db.Column(db.String(80))
    # vvv Is this a thing? db.Double? Cuz I honestly don't know.
    height = db.Column(db.Float)
    # vvv Maybe represent these two (allergies and diet) as lists that you can add new elements to? Is that possible in SQL?
    # ^^^ Should be! Or maybe use a JSon file(?) which is apparently the same thing but for databases?
    allergies = db.Column(db.String(120))
    dietRestrictions = db.Column(db.String(120))
    studentIDNumber = db.Column(db.Integer)
    phoneNumber = db.Column(db.Integer)
    carCapacity = db.Column(db.Integer)
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
        self.height = float(inputData['height'][:]) #height
        self.allergies = str(inputData['allergies'][:]) #allergies
        self.dietRestrictions = str(inputData['dietRestrictions'][:]) #dietRestrictions
        self.studentIDNumber = int(inputData['studentIDNumber'][:]) #studentIDNumber
        self.phoneNumber = int(inputData['phoneNumber'][:]) #phoneNumber
        self.carCapacity = int(inputData['carCapacity'][:]) #capCapacity
        # Also given a picture. That's neat. How to access it?

    def __repr__(self):
        #return '<User %r, ID: >' % self.username
        return '<User ' + self.username + ', ID: ' + self.googleNum + '>'

    def modifyAccount(self, rawData):
        # memes
        data = json.loads(rawData)
        print('Insert a thing here! Produce a spreadsheet already filled with the users information, then have it resubmit to this function.')
        self.username = str(data['username'][:])  # username
        self.email = str(data['email'][:])  # email # Not given, surprisingly? Ask Alasdair about this.
        self.firstName = str(data['firstName'][:])  # Given
        self.lastName = str(data['lastName'][:])  # Given
        self.age = int(data['age'][:])  # age
        self.height = float(data['height'][:])  # height
        self.allergies = str(data['allergies'][:])  # allergies
        self.dietRestrictions = str(data['dietRestrictions'][:])  # dietRestrictions
        self.studentIDNumber = int(data['studentIDNumber'][:])  # studentIDNumber
        self.phoneNumber = int(data['phoneNumber'][:])  # phoneNumber
        self.carCapacity = int(data['carCapacity'][:])  # capCapacity

    def accessData(self):
        dataDict = {
            'googleNum' : str(self.googleNum)[:],
            'username' : str(self.username)[:],
            'email' : str(self.email)[:],
        }
        data = json.dumps(dataDict)
        return data

def newUser(inputData):
    generatedUser = Account(inputData)
    return generatedUser

# Ask Alasdair what the @app.route thing does again, then WRITE IT DOWN.
# You should never have to call main(), apparently. That happens on its own.
@app.route('/', methods=['GET','POST'])
def main():
    #db.session.add(newUser('Joe', 'Joes email'))
    # db.session.add(newUser('Bob', 'Bobs email')) user/1231424324321421
    db.session.commit()
    print(Account.query.all())
    print(str(Account.query.all()[0].accessData()))
    return str(
        # Account.query.all()[0].__dict__
        #"<html> <h1>Hello World</h1></html>"
        'hi'
    )

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


def sampleConstructor():
    sampleData = {
        'family_name' : 'Vonallmen',
        'locale' : 'en',
        'name' : 'Matthew Vonallmen',
        'picture' : 'badmeme.jpg',
        'given_name' : 'Matthew',
        'id' : '123456789'
    }
    transportData = json.dumps(sampleData)
    #createAccount(transportData)

if __name__=='__main__':
    print('Creating a database...')
    if os.path.exists(currentPath + '/' + databaseName):
        print('God is dead and WE HAVE KILLED HIM!')
    else:
        with app.app_context():
            db.create_all()
        #sampleConstructor()
    # What does it mean when the app is "running?"
    # How do you display things on screen? Like, the website screen?
    #app.run()


# vvv How to select individual stuff.
#User.query.filter_by(id=1).all()
#User.query.filter_by(id=1).all()