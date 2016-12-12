
import sqlite3
import datetime
#TODO create functions that create the SQLite calls that fill in database from the forms ie calculate additonal info geo location weather and costs
#TODO get shota to write tests for all of this

MASTER_DB_ORDER = ['Trip_Name','Departure_Date', 'Return_Date', 'Trip_Location']
MASTERDBCOMAND = 'insert into Master (Trip_Name, Deparure_Date,Return_Date,Trip_Location, Details_Short, Post_Time, Participant_num, Partcipant_cap) VALUES (?,?,?,?,?,?,?,?)'

# TODO: Create DB Order using weather API and get the key stuff to work once this works play with deleting and creating trips in the db get those comands straight and then we will be good
TRIPS_DB_ORDER = ['Details', 'Coordinator_Name', 'Coordinator_Email', 'Coordinator_Phone', 'Gear_List', 'Trip_Meeting_Place', 'Additonal_Costs', 'Cost_BreakDown', 'Substance_Free']
TRIPSDBCOMAND = 'insert into Trips (Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone, Gear_List, Trip_Meeting_Place, Additional_Costs, Cost_BreakDown, Substance_Frre, Total_Cost, Weather_Forcast, Master_Key) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'

# TODO: Create DB orderer for this aswell o Kendrick lamr gettign sexy
PARTICIPANT_DB_ORDER = ['Participant', 'Phone', 'Driver', 'Car_Capacity']
PARTICIPANTDBCOMAND = 'insert into Participants (Trips_Key, Participant, Phone, Driver, Car_Capacity) VALUES (?,?,?,?,?)'


def AddTrip(form):
    """'
    used to construct the db insert for the trip table
    :param form is the form from POAForms class  MakeTripFormPOA
    :return: List of info for table
    """
    Master = MakeMaster(form)
    Trip = []
    Participants = []
    return Master, Trip, Participants
def MakeMaster(form):
    """
    :param form: form is the form from POAForms class  MakeTripFormPOA will create the row for Master table
    :return: List for creating Master row in table
    """
    Master = []
    for index in MASTER_DB_ORDER:
        Master += [str(form[index])]
    Master += [MakeShortDetails(form['Details'])]
    Master += [str(datetime.datetime.now())]
    Master += [1]
    Master += [form['Car_Capacity'] -1]
    return Master

def MakeShortDetails(Details):
    """
    :param Details:
    :return: A short version of details
    """
    if len(Details) > 100:
        return Details[:100] + '...'
    else:
        return Details[:int(len(Details)/2)] + '...'




form = {'GearList': 'All the things', 'Additional_Cost': '10', 'Departure_Date': datetime.date(2016, 12, 2), 'Car_Cap': 3, 'Car_Capacity': 5, 'Return_Date': datetime.date(2016, 12, 2), 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': '10 USD for strip club', 'Substance_Free': True, 'Coordinator_Phone': 9193975206, 'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_Meeting_Place': 'Service Road', 'Trip_Location': 'Red Rocks', 'submit': True, 'Details': 'Fuck bitches get monney'}
print(MakeMaster(form))

# app = Flask(__name__)

# wont work becuese DATABASE is configed in our app Im sure there is a work around but I am under time pressuere rn
# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
#
# # Calls connect DB
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
#
# def init_db():
#     """
#     will go to the schema flile
#     :return: VOID
#     """
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
#
# def show_entries(SQL):
#     """
#     Example show_entries('select title, text from entries order by id desc')
#     :param SQL: SQL code that will call table info to be returned
#     :return: entries form sql table look up
#     """
#     db = get_db()
#     cur = db.execute(SQL)
#     entries = cur.fetchall()
#     return entries