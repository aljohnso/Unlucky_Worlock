import unittest, datetime
from DatabaseConnection.DatabaseSubmissionConstructors import ParticipantCommandConstructor, TripCommandConstructor, MasterCommandConstructor

class DatabaseConstructorTests(unittest.TestCase):
    testParticipant_AJ = {'Participant': "alasdair Johnson", 'Phone': 9193975206, 'Driver': 1, 'Car_Capacity': 5}
    testParticipant_JL = {'Participant': "Jessie Levine", 'Phone': 2523456439, 'Driver': 0, 'Car_Capacity': 0}
    testInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206,
                 'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10,
                 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club',
                 'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 3, 'Substance_Free': False,
                 'Trip_Location': 'National Conservation Area, Las Vegas', 'Departure_Date': datetime.date(2016, 10, 12),
                 'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'NV'}

    def test_ParticpantCommandConstructor(self):
        particpant = ParticipantCommandConstructor(DatabaseConstructorTests.testParticipant_AJ, 1).participant
        print(particpant)
        expected_particpant = [1, "alasdair Johnson", "9193975206", "1", "5"]
        self.assertEqual(particpant, expected_particpant)#couldn cause error with the 1 being int we will see

    def test_MakeTripComandConstructor(self):
        makeTrip = TripCommandConstructor(DatabaseConstructorTests.testInput, 1)
        trip = makeTrip.trip
        location = DatabaseConstructorTests.testInput['Trip_Location'] + ', ' + DatabaseConstructorTests.testInput['Trip_State']
        locationData = makeTrip.getGoogleMapsData(Location=location)
        weather = makeTrip.getWeather(locationData)
        expected_trip = ['Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', '9193975206',
                         'All the things', 'Service Road', '10', 'cash for strip club', '3',0, 92.62, str(weather), 1]
        self.assertEqual(trip, expected_trip)

    def test_MasterCommandConstructor(self):
        master = MasterCommandConstructor(DatabaseConstructorTests.testInput).master
        print(master)
        expected_master = ['Red Rocks', '2016-10-12', '2016-12-12','National Conservation Area, Las Vegas, NV', 'Turn up and climb', str(datetime.date.today()), 1, 2]
        self.assertEqual(master, expected_master)


if __name__ == '__main__':
    unittest.main()
