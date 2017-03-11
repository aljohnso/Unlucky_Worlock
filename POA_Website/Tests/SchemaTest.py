import unittest
from DatabaseConnection.DataBaseSchema import Master, Trips, Participants, TripModel
Inputs = {'testParticipant_AJ':{'Participant': "alasdair Johnson",
                      'Email': 'aljohnso@students.pitzer.edu', 'Phone':9193975206, 'Driver': 1, 'Car_Capacity': 5},
     'testParticipant_JL' : {'Participant': "Jessie Levine",
                      'Email': 'jlenvin@gmail.com', 'Phone': 2523456439, 'Driver': 0, 'Car_Capacity': 0},
     'testParticipant_JJ' : {'Participant': "JoAnn Johnson",
                      'Email': 'jJohnson@gmail.com', 'Phone': 9913975206, 'Driver': 0, 'Car_Capacity': 0},
     'CorrecttestInputRedRocks':{'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206,
                    'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10,
                    'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club',
                    'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 3, 'Substance_Free': False,
                    'Trip_Location': 'National Conservation Area, Las Vegas',
                    'Departure_Date': datetime.date(2016, 10, 12),
                    'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'NV'},
     'IncorrecttestInpuRedRocks' : {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things',
                      'Coordinator_Phone': 9193975206,
                      'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10,
                      'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club',
                      'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 3, 'Substance_Free': False,
                      'Trip_Location': 'the middle of knower 123423421', 'Departure_Date': datetime.date(2016, 10, 12),
                      'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'ZX'}}


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
