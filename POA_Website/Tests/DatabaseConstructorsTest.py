import unittest, datetime
from DatabaseConnection.DatabaseSubmissionConstructors import ParticipantConstructor, TripConstructor, MasterConstructor

class DatabaseConstructorTests(unittest.TestCase):
    testParticipant_AJ = {'Participant': "alasdair Johnson",'Email': 'aljohnso@students.pitzer.edu', 'Phone': 9193975206, 'Driver': 1, 'Car_Capacity': 5}
    CorrecttestInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206,
                 'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10,
                 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club',
                 'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 3, 'Substance_Free': False,
                 'Trip_Location': 'National Conservation Area, Las Vegas', 'Departure_Date': datetime.date(2016, 10, 12),
                        'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'NV'}
    #Discribes a correct input from form
    IncorrecttestInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206,
                 'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10,
                 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club',
                 'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 3, 'Substance_Free': False,
                 'Trip_Location': '', 'Departure_Date': datetime.date(2016, 10, 12),
                        'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': ''}
    def test_ParticpantCommandConstructor(self):
        particpant = ParticipantConstructor(DatabaseConstructorTests.testParticipant_AJ, 1).participant
        print(particpant)
        expected_particpant = {'Participant': 'alasdair Johnson', 'Car_Capacity': 5,
                               'Master_Key': 1, 'Driver': 1, 'Phone': 9193975206,
                               'Email': 'aljohnso@students.pitzer.edu'}
        #expected_particpant = [1, 'alasdair Johnson', 'aljohnso@students.pitzer.edu', '9193975206', '1', '5']
        self.assertDictEqual(particpant, expected_particpant)#couldn cause error with the 1 being int we will see

    def test_MakeTripComandConstructor(self):
        """
        Tests Make trip constructior with all valid inputs
        """
        makeTrip = TripConstructor(DatabaseConstructorTests.CorrecttestInput, 1)
        trip = makeTrip.trip
        cordinator = makeTrip.leader
        location = DatabaseConstructorTests.CorrecttestInput['Trip_Location'] + ', ' + DatabaseConstructorTests.CorrecttestInput['Trip_State']
        locationData = makeTrip.getGoogleMapsData(Location=location)
        weather = makeTrip.getWeather(locationData)
        expected_trip = {'GearList': 'All the things',
         'Weather_Forcast':  str(weather),
         'Master_Key': 1, 'Coordinator_Email': 'aljohnso@students.pitzer.edu',
         'Trip_Meeting_Place': 'Service Road', 'Substance_Free': 0, 'Details': 'Turn up and climb',
         'Additional_Cost': 10, 'Cost_Breakdown': 'cash for strip club', 'Total_Cost': 92.62,
        'Coordinator_Name': 'Alasdair Johnson', 'Coordinator_Phone': 9193975206}
        expected_particpant = {'Participant': 'alasdair Johnson', 'Car_Capacity': 3,
                               'Master_Key': 1, 'Driver': 1, 'Phone': 9193975206,
                               'Email': 'aljohnso@students.pitzer.edu'}
        #expected_trip = ['Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', '9193975206',
                         #'All the things', 'Service Road', '10', 'cash for strip club', '3',0, 92.62, str(weather), 1]
        self.assertDictEqual(trip, expected_trip)
        self.assertDictEqual(cordinator, expected_particpant)

    def test_TripIncorrectLocation(self):
        """
        Tests make trip when google maps returns and invalid location / no location, this will discribe cases
        where users give location in incorrect location.
        """
        makeTrip = TripConstructor(DatabaseConstructorTests.CorrecttestInput, 1)
        trip = makeTrip.trip
        cordinator = makeTrip.leader

        expected_trip = {'GearList': 'All the things',
         'Weather_Forcast':  "",
         'Master_Key': 1, 'Coordinator_Email': 'aljohnso@students.pitzer.edu',
         'Trip_Meeting_Place': 'Service Road', 'Substance_Free': 0, 'Details': 'Turn up and climb',
         'Additional_Cost': 10, 'Cost_Breakdown': 'cash for strip club', 'Total_Cost': 10,
         'Coordinator_Name': 'Alasdair Johnson', 'Coordinator_Phone': 9193975206}
        expected_particpant = {'Participant': 'alasdair Johnson', 'Car_Capacity': 5,
                               'Master_Key': 1, 'Driver': 1, 'Phone': 9193975206,
                               'Email': 'aljohnso@students.pitzer.edu'}
        self.assertDictEqual(trip, expected_trip)
        self.assertDictEqual(cordinator, expected_particpant)

    def test_MasterCommandConstructor(self):
        master = MasterConstructor(DatabaseConstructorTests.CorrecttestInput).master
        print(master)
        expected_master = {'Details': 'Turn up and climb', 'Departure_Date': datetime.date(2016, 10, 12), 'Post_Time': datetime.date.today(),
         'Trip_Name': 'Red Rocks', 'Participant_num': 1, 'Return_Date': datetime.date(2016, 12, 12), 'Car_Capacity': 3,
         'Trip_Location': 'National Conservation Area, Las Vegas, NV', 'Car_Cap':3, 'Car_Num':1}
        self.assertDictEqual(master, expected_master)

    #TODO: consider when particpant raises keyerror case



if __name__ == '__main__':
    unittest.main()
