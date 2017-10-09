import datetime,requests, re

class MasterConstructor:
    def __init__(self, form):
        """
        :param form:
        Will take in form and create a list that can be executed to put in database
        """
        self.master = self.MakeMaster(form)

    def MakeMaster(self, form):
        """
        :param form: form is the form from POAForms class  MakeTripFormPOA will create the row for Master table
        :return: Dictionary for creating Master row in table
        """
        Master = {} # consider using dict.values()
        Master["Trip_Name"] = form["tripName"]
        Master["Departure_Date"] = form["departureDate"]
        Master["Return_Date"] = form["returnDate"]
        Master['Trip_Location'] = form['tripLocation'] + ', ' + form['tripState']
        Master['Details'] = self.MakeShortDetails(str(form['details']))
        Master['Post_Time'] = datetime.date.today()
        Master['Participant_num'] = 1
        Master['Car_Cap'] = form['maxCars']
        if form['driver']:
            Master['Car_Num'] = 1
        else:
            Master['Car_Num'] = 0
        return Master

    def MakeShortDetails(self, details):
        """
        :param details:
        :return: A short version of details
        """
        if len(details) > 100:
            return details[:100] + '...'
        else:
            return details



class TripConstructor:

    WUNDERGROUND_KEY = 'dd0fa4bc432d5dbd'

    def __init__(self, form, master_key):
        """
        :param form:
        Will take in form and create a list that can be executed to put in database
        """
        self.trip = self.MakeTrip(form, master_key)
        #self.leader = ParticipantConstructor(form, master_key).participant

    def MakeTrip(self, Form, master_key):
        """
        :param Form: form is the form from POAForms class  MakeTripFormPOA will create the row for Trip table
        :return: The List for creating row in trip table
        """
        Trip = {}
        location = str(Form['tripLocation'] + ',' + Form['tripState'])
        locationData = self.getGoogleMapsData(location)
        #for index in TripConstructor.TRIPS_DB_ORDER:
        #    Trip[index] = Form[index]
        #TRIPS_DB_ORDER = ['Details', 'GearList', 'Trip_Meeting_Place',
        #                  'Additional_Cost', 'Cost_Breakdown']
        Trip["Details"] = Form["details"]
        Trip["GearList"] = Form["gearList"]
        Trip["Trip_Meeting_Place"] = Form["meetingPlace"]
        # TODO: Bring the additional cost and cost breakdown entries into the 21st century.
        Trip["Costs"] = Form["costDict"]
        Trip["Costs"]["POAGasCost"] = self.getDistance(locationData) * 0.17 * 2
        # Trip["Additional_Cost"] = Form["costMagnitude"]
        # Trip["Cost_Breakdown"] = Form["costMagnitude"]
        # distance = self.getDistance(locationData)
        # total_Cost = distance*.17*2 + int(Form['costMagnitude'])
        Trip["Substance_Free"] = Form["substanceFree"]
        # TODO: make these into lists or something, current code should break. People's arms. Arms will be broken.
        # Trip['Additional_Cost'] = int(Form['costMagnitude'])
        # Trip["Total_Cost"] = total_Cost
        Trip["Weather_Forcast"] = str(self.getWeather(locationData))
        Trip["Master_Key"] = master_key
        # print(Trip)
        return Trip

    def getDistance(self, LocationData):
        """
        Will try if the data is not valid will return 0
        :param LocationData: Google maps API Return
        :return: Distance
        """
        try:
            return float(LocationData['rows'][0]['elements'][0]['distance']['text'][:-3])
        except:
            return 0

    def getWeather(self, GoogleMapsData):
        """
        :param GoogleMapsData: A tuple with the location with index 0 being the state and index 1 being the city or location
        :return:
        """
        try:
            URL = 'http://api.wunderground.com/api/dd0fa4bc432d5dbd/forecast10day/q/'
            # Location = GoogleMapsData['destination_addresses'][0].split(",")
            # # this could produce an error if they give us a city as well as adress and state
            # # print(Location)
            # state = Location[1][1:3]
            # place = "_".join(Location[0].split(" "))
            # # print(state, place)
            # data = requests.get(URL + state + '/' + place + '.json').json()
            Location = GoogleMapsData['destination_addresses'][0]
            pattern = '(\d{5}([\-]\d{4})?)'#regex for zipcode
            zipcode = re.search(pattern, Location).group(1)
            data = requests.get(URL + zipcode + '.json').json()
            return data['forecast']['simpleforecast']  # gives 10 day forcast as a list of dicts
        except:
            return ""

    def getGoogleMapsData(self, Location):
        try:
            pitzerCollege = '1050 N Mills Ave,Claremont,CA'
            url = "http://maps.googleapis.com/maps/api/distancematrix/json"
            params = {'origins': pitzerCollege, 'destinations': Location, 'mode': 'driving', 'units': 'imperial'}
            response = requests.get(url, params=params)
            data = response.json()
            # print(data)
            return data
        except:
            return None


class ParticipantConstructor:
    PARTICIPANT_DB_ORDER = ['Participant','Email', 'Phone', 'Driver', 'Car_Capacity']

    def __init__(self, form, MasterID):
        """
        :param form:
        Will take in form and create a list that can be executed to put in database
        """
        self.participant = self.Makeparticipant(form, MasterID)

    def Makeparticipant(self, Form, MasterID):
        """
        :param Form: form from POAForms class that details
        :return:
        """
        participant = {"Master_Key":MasterID}
        try:
            for index in ParticipantConstructor.PARTICIPANT_DB_ORDER:
                participant[index] = Form[index]
            # print(Form.values())
            # print(participant)
        except KeyError:
            participant['Participant'] = Form['Coordinator_Name']
            participant['Email'] = Form['Coordinator_Email']
            participant['Phone'] = Form['Coordinator_Phone']
            if Form['Car_Capacity'] != 0:
                participant['Driver'] = 1
            else:
                participant['Driver'] = 0
            participant['Car_Capacity'] = Form['Car_Capacity']
            # print(Form.values())
            # print(participant)
        return participant





