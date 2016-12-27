
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
    print("DEPRICATED USE DatabaseConnection.DatabaseConnection" )
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
    print("DEPRICATED USE DatabaseConnection.DatabaseConnection")
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
    print("DEPRICATED USE DatabaseConnection.DatabaseConnection")
    if len(Details) > 100:
        return Details[:100] + '...'
    else:
        return Details[:int(len(Details)/2)] + '...'

def MakeTrip(Form, db):
    """
    :param Form: form is the form from POAForms class  MakeTripFormPOA will create the row for Trip table
    :return: The List for creating row in trip table
    """
    print("DEPRICATED USE DatabaseConnection.DatabaseConnection")
    Trip = []
    location = str(Form['Trip_Location'] + ',' + Form['Trip_State'])
    locationData = getGoogleMapsData(location)
    for index in TRIPS_DB_ORDER:
        Trip += [str(Form[index])]
    distance = float(locationData['rows'][0]['elements'][0]['distance']['text'][:-3])
    total_Cost = distance*.17 + Form['Additional_Cost']
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
     print("DEPRICATED USE DatabaseConnection.DatabaseConnection")
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
    print("DEPRICATED USE DatabaseConnection.DatabaseConnection")
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
    print("DEPRICATED USE DatabaseConnection.DatabaseConnection")
    pitzerCollege= '1050 N Mills,Ave,Claremont,CA'
    url = "http://maps.googleapis.com/maps/api/distancematrix/json"
    params = {'origins':pitzerCollege, 'destinations': Location, 'mode': 'driving', 'units': 'imperial'}
    response = requests.get(url,params=params)
    data = response.json()
    print(data)
    return data

def deleteTrip(TripID):
    """
    Will Delete trip from database based on trip ID from Master Table and Trips Table
    :param TripID:
    :return: None
    """
    #TODO: Implement
    pass
