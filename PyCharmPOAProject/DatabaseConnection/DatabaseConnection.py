import sqlite3, requests, datetime


class DatabaseConnection:
    """
        This class contains all maniputaltion fuctions for the database by intializing the object we open the database
        Assumes POA Schema 12-26-16 CHANGE IF UPDATED

    """
    MASTER_DB_ORDER = ['Trip_Name', 'Departure_Date', 'Return_Date', 'Trip_Location']
    MASTERDBCOMAND = 'insert into Master (Trip_Name, Deparure_Date,Return_Date,Trip_Location, Details_Short, ' \
                     'Post_Time, Participant_num, Partcipant_cap) VALUES (?,?,?,?,?,?,?,?)'
    TRIPS_DB_ORDER = ['Details', 'Coordinator_Name', 'Coordinator_Email', 'Coordinator_Phone', 'GearList',
                      'Trip_Meeting_Place', 'Additional_Cost', 'Cost_Breakdown', 'Car_Cap']
    TRIPSDBCOMAND = 'insert into Trips (Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone, ' \
                    'Gear_List, Trip_Meeting_Place, Additional_Costs, Cost_BreakDown, Car_Cap, Substance_Frre, Total_Cost, Weather_Forcast, Master_Key) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'
    PARTICIPANT_DB_ORDER = ['Participant', 'Phone', 'Driver', 'Car_Capacity']
    PARTICIPANTDBCOMAND = 'insert into Participants (Trips_Key, Participant, Phone, Driver, Car_Capacity) VALUES (?,?,?,?,?)'
    WUNDERGROUND_KEY = 'dd0fa4bc432d5dbd'

    def __init__(self, path):
        """
            Will create Datbase Connection
        """
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def closeConnection(self):
        self.connection.close()

    def AddTrip(self, form):
        """'
        used to construct the db insert for the trip table
        :param form is the form from POAForms class  MakeTripFormPOA
        :return: List of info for table
        """
        Master = self.MakeMaster(form)
        # print(Master)
        self.cursor.execute(DatabaseConnection.MASTERDBCOMAND, Master)
        Trip = self.MakeTrip(form)
        # print(Trip)
        # print(TRIPSDBCOMAND)
        self.cursor.execute(DatabaseConnection.TRIPSDBCOMAND, Trip)
        self.connection.commit()

    def MakeMaster(self, form):
        """
        :param form: form is the form from POAForms class  MakeTripFormPOA will create the row for Master table
        :return: List for creating Master row in table
        """
        Master = []
        for index in DatabaseConnection.MASTER_DB_ORDER:
            Master += [str(form[index])]
        Master += [self.MakeShortDetails(form['Details'])]
        Master += [str(datetime.datetime.now())]
        Master += [1]
        Master += [form['Car_Capacity'] - 1]
        return Master

    def MakeShortDetails(self, Details):
        """
        :param Details:
        :return: A short version of details
        """
        if len(Details) > 100:
            return Details[:100] + '...'
        else:
            return Details[:int(len(Details) / 2)] + '...'

    def MakeTrip(self, Form):
        """
        :param Form: form is the form from POAForms class  MakeTripFormPOA will create the row for Trip table
        :return: The List for creating row in trip table
        """
        Trip = []
        location = str(Form['Trip_Location'] + ',' + Form['Trip_State'])
        locationData = self.getGoogleMapsData(location)
        for index in DatabaseConnection.TRIPS_DB_ORDER:
            Trip += [str(Form[index])]
        distance = float(locationData['rows'][0]['elements'][0]['distance']['text'][:-3])
        total_Cost = distance * .17 + Form['Additional_Cost']
        Trip += [int(Form["Substance_Free"])]
        Trip += [total_Cost]
        Trip += [str(self.getWeather(locationData))]
        Trip += [self.cursor.lastrowid]
        return Trip

    def Makeparticipant(self, Form):
        """
        :param Form: form from POAForms class that details
        :return:
        """
        participant = []
        for index in DatabaseConnection.PARTICIPANT_DB_ORDER:
            participant += [str(Form[index])]
        participant += []

    def getWeather(self, GoogleMapsData):
        """
        :param GoogleMapsData: A tuple with the location with index 0 being the state and index 1 being the city or location
        :return:
        """
        try:
            URL = 'http://api.wunderground.com/api/dd0fa4bc432d5dbd/forecast10day/q/'
            Location = GoogleMapsData['destination_addresses'][0].split(
                ",")  # this could produce an error if they give us a city as well as adress and state
            # print(Location)
            state = Location[1][1:3]
            place = "_".join(Location[0].split(" "))
            # print(state, place)
            data = requests.get(URL + state + '/' + place + '.json').json()
            return data['forecast']['simpleforecast']  # gives 10 day forcast as a list of dicts
        except:
            raise Exception("Location format is not correct")
            return None

    def getGoogleMapsData(self, Location):
        pitzerCollege = '1050 N Mills,Ave,Claremont,CA'
        url = "http://maps.googleapis.com/maps/api/distancematrix/json"
        params = {'origins': pitzerCollege, 'destinations': Location, 'mode': 'driving', 'units': 'imperial'}
        response = requests.get(url, params=params)
        data = response.json()
        print(data)
        return data


    def deleteTrip(self, TripID):
        """
        Will Delete trip from database based on trip ID from Master Table and Trips Table
        :param TripID:
        :return: None
        """
        self.cursor.execute('DELETE FROM Master WHERE id=' +  str(TripID))
        self.connection.commit()


