
import sqlite3, requests, datetime

#TODO create functions that create the SQLite calls that fill in database from the forms ie calculate additonal info geo location weather and costs
#TODO get shota to write tests for all of this

MASTER_DB_ORDER = ['Trip_Name','Departure_Date', 'Return_Date', 'Trip_Location']
MASTERDBCOMAND = 'insert into Master (Trip_Name, Deparure_Date,Return_Date,Trip_Location, Details_Short, Post_Time, Participant_num, Partcipant_cap) VALUES (?,?,?,?,?,?,?,?)'

# TODO: Create DB Order using weather API and get the key stuff to work once this works play with deleting and creating trips in the db get those comands straight and then we will be good
TRIPS_DB_ORDER = ['Details', 'Coordinator_Name', 'Coordinator_Email', 'Coordinator_Phone', 'GearList', 'Trip_Meeting_Place', 'Additional_Cost', 'Cost_Breakdown', 'Car_Cap']
TRIPSDBCOMAND = 'insert into Trips (Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone, Gear_List, Trip_Meeting_Place, Additional_Costs, Cost_BreakDown, Car_Cap, Substance_Frre, Total_Cost, Weather_Forcast, Master_Key) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'

# TODO: Create DB orderer for this aswell o Kendrick lamr gettign sexy
PARTICIPANT_DB_ORDER = ['Participant', 'Phone', 'Driver', 'Car_Capacity']
PARTICIPANTDBCOMAND = 'insert into Participants (Trips_Key, Participant, Phone, Driver, Car_Capacity) VALUES (?,?,?,?,?)'
WUNDERGROUND_KEY = 'dd0fa4bc432d5dbd'



def AddTrip(form, db):
    """'
    used to construct the db insert for the trip table
    :param form is the form from POAForms class  MakeTripFormPOA
    :return: List of info for table
    """
    dbc =db.cursor()
    Master = MakeMaster(form)
    # print(Master)
    dbc.execute(MASTERDBCOMAND, Master)
    # db.commit()
    Trip = MakeTrip(form, dbc)
    print(Trip)
    print(TRIPSDBCOMAND)
    dbc.execute(TRIPSDBCOMAND, Trip)
    db.commit()
    # return Master, Trip
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

def MakeTrip(Form, db):
    """
    :param Form: form is the form from POAForms class  MakeTripFormPOA will create the row for Trip table
    :return: The List for creating row in trip table
    """
    Trip = []
    location = str(Form['Trip_Location'] + ',' + Form['Trip_State'])
    locationData = getGoogleMapsData(location)
    for index in TRIPS_DB_ORDER:
        Trip += [str(Form[index])]
    distance = float(locationData['rows'][0]['elements'][0]['distance']['text'][:-3])
    total_Cost = distance*.35 + Form['Additional_Cost']
    Trip += [int(Form["Substance_Free"])]
    Trip += [total_Cost]
    Trip += [str(getWeather(locationData))]
    Trip += [db.lastrowid]
    return Trip


def Makeparticipant(Form, db):
     """
     :param Form: form from POAForms class that details
     :param db: datebase connection
     :return:
     """
     participant = []
     for index in PARTICIPANT_DB_ORDER:
         participant += [str(Form[index])]
     participant += []

# def getTripForParticipant()

def getWeather(GoogleMapsData):
    """
    :param GoogleMapsData: A tuple with the location with index 0 being the state and index 1 being the city or location
    :return:
    """
    try:
        URL = 'http://api.wunderground.com/api/dd0fa4bc432d5dbd/forecast10day/q/'
        Location = GoogleMapsData['destination_addresses'][0].split(",")  # this could produce an error if they give us a city as well as adress and state
        # print(Location)
        state = Location[1][1:3]
        place = "_".join(Location[0].split(" "))
        # print(state, place)
        data = requests.get(URL + state + '/' + place  + '.json').json()
        return data['forecast']['simpleforecast']  # gives 10 day forcast as a list of dicts
    except:
        raise Exception("Location format is not correct")
        return None

def getGoogleMapsData(Location):
    pitzerCollege= '1050 N Mills,Ave,Claremont,CA'
    url = "http://maps.googleapis.com/maps/api/distancematrix/json"
    params = {'origins':pitzerCollege, 'destinations': Location, 'mode': 'driving', 'units': 'imperial'}
    response = requests.get(url,params=params)
    data = response.json()
    print(data)
    return data


#*************************************************
#*************************************************
#               TESTS
#*************************************************
#*************************************************
# conn = sqlite3.connect('example.db')
# c = conn.cursor()
def makeTestTables(conn):
    conn.execute('drop table if exists Trips;' )
    conn.execute('CREATE TABLE Trips(id INTEGER PRIMARY KEY AUTOINCREMENT,Master_Key integer not NULL,Details TEXT not NULL,Coordinator_Name TEXT not NULL,Coordinator_Email TEXT not NULL,Coordinator_Phone Integer not NULL,Gear_List TEXT not NULL,Trip_Meeting_Place TEXT not NULL,Additional_Costs Integer not NULL,Total_Cost Integer NOT NULL,Cost_BreakDown Text NOT NULL,Car_Cap Integer NOT NULL,Substance_Frre Integer NOT NULL,Weather_Forcast blob NOT NULL,FOREIGN KEY(Master_Key) REFERENCES Master(id));')
    conn.execute('drop table if exists Master;')
    conn.execute('create TABLE Master (id integer PRIMARY KEY AUTOINCREMENT ,Trip_Name TEXT not NULL,Deparure_Date TEXT not NULL,Return_Date TEXT not NULL,Details_Short TEXT not NULL,Post_Time TEXT not NULL,Participant_num Integer not Null,Partcipant_cap  Integer not NULL,Trip_Location Integer NOT NULL);')
    conn.commit()

def Tests(conn):
    form = {'GearList': 'All the things', 'Additional_Cost': 10,'Trip_State': 'CA', 'Departure_Date': datetime.date(2016, 12, 2), 'Car_Cap': 3, 'Car_Capacity': 5, 'Return_Date': datetime.date(2016, 12, 2), 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': '10 USD for strip club', 'Substance_Free': True, 'Coordinator_Phone': 9193975206, 'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_Meeting_Place': 'Service Road', 'Trip_Location': 'Joshua Tree', 'submit': True, 'Details': 'Fuck bitches get monney'}
    AddTrip(form, conn)
    # print(MakeTrip(form, c))
    # print(MakeMaster(form))
    # print(MakeLocation(form))
    # print(getWeather(('CA', 'Joshua_Tree')))
    # print(getGoogleMapsData('Red Rocks, NV'))
