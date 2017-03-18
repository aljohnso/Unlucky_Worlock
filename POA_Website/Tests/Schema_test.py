import unittest, datetime
from DatabaseConnection.DataBaseSchema import Master, Trips, Participants, TripModel, db
Inputs = {'testParticipant_AJ':{'Participant': "alasdair Johnson",
                      'Email': 'aljohnso@students.pitzer.edu', 'Phone':9193975206, 'Driver': 1, 'Car_Capacity': 3},
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

expected_trip = {'GearList': 'All the things',
                 'Weather_Forcast': "",
                 'Master_Key': 1, 'Coordinator_Email': 'aljohnso@students.pitzer.edu',
                 'Trip_Meeting_Place': 'Service Road', 'Substance_Free': 0, 'Details': 'Turn up and climb',
                 'Additional_Cost': 10, 'Cost_Breakdown': 'cash for strip club', 'Total_Cost':  92.62,
                 'Coordinator_Name': 'Alasdair Johnson', 'Coordinator_Phone': 9193975206}


class MyTestCase(unittest.TestCase):

    def test_Master(self):
        expected_master = {'Details_Short': 'Turn up and climb', 'Departure_Date': datetime.date(2016, 10, 12),
                           'Post_Time': datetime.date.today(),
                           'Trip_Name': 'Red Rocks', 'Participant_num': 1, 'Return_Date': datetime.date(2016, 12, 12),
                           'Participant_cap': 3,
                           'Trip_Location': 'National Conservation Area, Las Vegas, NV', 'Car_Cap': 3, 'Car_Num': 1}
        input = Inputs['CorrecttestInputRedRocks']
        out = Master(input).__dict__
        out.pop('_sa_instance_state', None)
        print(out)
        self.assertDictEqual(out, expected_master)

    def test_Trips(self):
        input = Inputs['CorrecttestInputRedRocks']
        out = Trips(input, 1).__dict__
        out.pop('_sa_instance_state', None)
        out['Weather_Forecast'] = "" # Take out forcast as this is checked in Constructor tests
        expected_trip = {'Gear_List': 'All the things',
                         'Weather_Forecast': "",
                         'Master_Key': 1, 'Coordinator_Email': 'aljohnso@students.pitzer.edu',
                         'Trip_Meeting_Place': 'Service Road', 'Substance_Free': 0, 'Details': 'Turn up and climb',
                         'Additional_Costs': 10, 'Cost_BreakDown': 'cash for strip club', 'Total_Cost': 92.62,
                         'Coordinator_Name': 'Alasdair Johnson', 'Coordinator_Phone': 9193975206}
        print(out)
        self.assertDictEqual(out, expected_trip)

    def test_Participants(self):
        input = Inputs['testParticipant_AJ']
        out = Participants(input, 1).__dict__
        out.pop('_sa_instance_state', None)
        expected_particpant = {'Participant': 'alasdair Johnson', 'Car_Capacity': 3,
                               'Master_Key': 1, 'Driver': 1, 'Phone': 9193975206,
                               'Email': 'aljohnso@students.pitzer.edu'}
        self.assertDictEqual(out, expected_particpant)

    def test_ParticipantsLeader(self):
        input = Inputs['CorrecttestInputRedRocks']
        out = Participants(input, 1).__dict__
        out.pop('_sa_instance_state', None)
        expected_particpant = {'Participant': 'Alasdair Johnson', 'Car_Capacity': 3,
                               'Master_Key': 1, 'Driver': 1, 'Phone': 9193975206,
                               'Email': 'aljohnso@students.pitzer.edu'}
        self.assertDictEqual(out, expected_particpant)




if __name__ == '__main__':
    unittest.main()
