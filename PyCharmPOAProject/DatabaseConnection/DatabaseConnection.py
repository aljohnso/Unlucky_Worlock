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
        print(Master)
        self.cursor.execute(DatabaseConnection.MASTERDBCOMAND, Master)
        Trip = self.MakeTrip(form)
        print(Trip)
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
        Master += [self.MakeShortDetails(str(form['Details']))]
        Master += [str(datetime.date.today())]
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
        # print(data)
        return data

    def deleteTrip(self, MasterID):
        """
        Will Delete trip from database based on trip ID from Master Table and Trips Table
        :param TripID:
        :return: None
        """

        self.cursor.execute('DELETE FROM Master WHERE id=' + str(MasterID))#wrong
        self.connection.commit()

    def checkTrip(self, server_time = datetime.datetime.now()):
        data = self.cursor.execute('select Deparure_Date, id from  Master order by id desc').fetchall()
        print('data passed to check')
        print(data)
        # counter = 1
        for ENTREE in data:
            departuredate = datetime.datetime.strptime(ENTREE[0], '%Y-%m-%d')
            print('checking entrie')
            print(server_time, departuredate)
            print(server_time >= departuredate)
            if server_time >= departuredate:# I dont understand this line --Alasdair
                index = data.index(ENTREE)
                print('deleting trip')
                # print(self.getTrip(index), index)
                print(ENTREE)
                self.cursor.execute('DELETE FROM Master WHERE id=' + str(ENTREE[1]))

                print()
            # counter += 1
        self.connection.commit()
        return self.cursor.execute('select * from  Master order by id desc').fetchall()

    def Makeparticipant(self, Form):
        """
        :param Form: form from POAForms class that details
        :return:
        """
        participant = []
        for index in DatabaseConnection.PARTICIPANT_DB_ORDER:
            participant += [str(Form[index])]
        return participant

    def Addparticipant(self, Form, tripID):
        participant = self.Makeparticipant(Form)
        # print(participant)
        participant.insert(0, tripID)
        # print(participant)
        self.cursor.execute(self.PARTICIPANTDBCOMAND, participant)
        self.connection.commit()

    def getParticipants(self, tripID):
        try:
            particpants = self.cursor.execute('SELECT * FROM Particpants WHERE Master_Key = ' + tripID)
            return particpants
        except:
            return None

    def deleteParticpant(self, participant_id):
        self.cursor.execute('DELETE FROM Participants WHERE id=' + str(participant_id))
        self.connection.commit()

    def getTrip(self,Master_Key):
        master_details = self.cursor.execute('select * from Master WHERE id =' + str(Master_Key)).fetchall()
        trip_details = self.cursor.execute('select * from Trips WHERE Master_Key =' + str(Master_Key)).fetchall()
        return trip_details, master_details









