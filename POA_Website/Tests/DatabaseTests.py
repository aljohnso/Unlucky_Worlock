
import unittest, os, datetime
from copy import deepcopy
from flask_testing import TestCase
from Pitzer_Outdoor_Adventure import app
from DatabaseConnection.DataBaseSchema import db, Master, Participants, Trips, TripModel
from DatabaseConnection.DatabaseQuery import POA_db_query

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

Expected = {'expected_particpant' : {'Participant': 'Alasdair Johnson', 'Car_Capacity': 3,
                               'Master_Key': 1, 'Driver': 1, 'Phone': 9193975206,
                               'Email': 'aljohnso@students.pitzer.edu', 'id':1},
        'expected_master' : {'Details_Short': 'Turn up and climb', 'Departure_Date': datetime.date(2016, 10, 12),
                           'Post_Time': datetime.date.today(),
                           'Trip_Name': 'Red Rocks', 'Participant_num': 1, 'Return_Date': datetime.date(2016, 12, 12),
                           'Participant_cap': 3,
                           'Trip_Location': 'National Conservation Area, Las Vegas, NV', 'Car_Cap': 3, 'Car_Num': 1, 'id':1},
        'expected_trip': {'Gear_List': 'All the things',
                         'Weather_Forecast': "",
                         'Master_Key': 1, 'Coordinator_Email': 'aljohnso@students.pitzer.edu',
                         'Trip_Meeting_Place': 'Service Road', 'Substance_Free': 0, 'Details': 'Turn up and climb',
                         'Additional_Costs': 10, 'Cost_BreakDown': 'cash for strip club', 'Total_Cost': 92.62,
                         'Coordinator_Name': 'Alasdair Johnson', 'Coordinator_Phone': 9193975206, 'id':1}}

class Database_Use_Tests(TestCase):

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/DataBase_Test_Scripts/testing.db'
    # TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_TripModel_Constructor(self):
        """
        asserts that TripModel Constructor works correctly
        """
        # create trip
        model = TripModel(Inputs['CorrecttestInputRedRocks'])

        # add to db
        db.session.add(model.master)
        db.session.add(model.trip)
        db.session.add(model.leader)
        # db.session.commit() #removed so database does not get full of stuff

        #queries
        masterInfo = deepcopy(Master.query.filter_by(id = 1).all()[0].__dict__)
        tripInfo = deepcopy(Trips.query.filter_by(Master_Key = 1).all()[0].__dict__)
        particpant_info = deepcopy(Participants.query.filter_by(Master_Key = 1).all()[0].__dict__)

        #remove unessary stuff for comparisons
        masterInfo.pop('_sa_instance_state', None)
        tripInfo.pop('_sa_instance_state', None)
        particpant_info.pop('_sa_instance_state', None)
        tripInfo['Weather_Forecast'] = "" # Take out forcast as this is checked in Constructor tests

        #Assertions
        self.assertDictEqual(Expected['expected_master'], masterInfo)#comparisons
        self.assertDictEqual(Expected['expected_particpant'],particpant_info)
        self.assertDictEqual(Expected['expected_trip'], tripInfo)

    def test_TripModel_addModel(self):
        """
        Standered adding trip op will assert that trip can be inserted and extraceted
        from db
        """
        # create trip
        model = TripModel(Inputs['CorrecttestInputRedRocks'])

        # add to db
        model.addModel()
        # db.session.commit() #removed so database does not get full of stuff

        #queries
        masterInfo = Master.query.filter_by(id = 1).all()[0].__dict__
        tripInfo = Trips.query.filter_by(Master_Key = 1).all()[0].__dict__
        particpant_info = Participants.query.filter_by(Master_Key = 1).all()[0].__dict__

        #remove unessary stuff for comparisons
        masterInfo.pop('_sa_instance_state', None)
        tripInfo.pop('_sa_instance_state', None)
        particpant_info.pop('_sa_instance_state', None)
        tripInfo['Weather_Forecast'] = "" # Take out forcast as this is checked in Constructor tests

        #Assertions
        self.assertDictEqual(Expected['expected_master'], masterInfo)#comparisons
        self.assertDictEqual(Expected['expected_particpant'],particpant_info)
        self.assertDictEqual(Expected['expected_trip'], tripInfo)

    def test_foren_key_relationships(self):
        """
        Tests to make sure cascade delete works ie delete master deletes all particpants and trip
        associated
        """
        # create trip
        model = TripModel(Inputs['CorrecttestInputRedRocks'])

        # add to db
        db.session.add(model.master)
        db.session.add(model.trip)
        db.session.add(model.leader)
        # db.session.commit() #removed so database does not get full of stuff

        #queries
        masterInfo = deepcopy(Master.query.filter_by(id = 1).all()[0].__dict__)
        tripInfo = deepcopy(Trips.query.filter_by(Master_Key = 1).all()[0].__dict__)
        particpant_info = deepcopy(Participants.query.filter_by(Master_Key = 1).all()[0].__dict__)

        #remove unessary stuff for comparisons
        masterInfo.pop('_sa_instance_state', None)
        tripInfo.pop('_sa_instance_state', None)
        particpant_info.pop('_sa_instance_state', None)
        tripInfo['Weather_Forecast'] = "" # Take out forcast as this is checked in Constructor tests

        #Assertions before delete lets make sure everying is the way we want
        self.assertDictEqual(Expected['expected_master'], masterInfo)#comparisons
        self.assertDictEqual(Expected['expected_particpant'],particpant_info)
        self.assertDictEqual(Expected['expected_trip'], tripInfo)

        JessieIsBae = Participants(Inputs['testParticipant_JL'], 1)
        for i in range(6):
            #Love u <3
            db.session.add(JessieIsBae)

        #delete master

        tripMaster = Master.query.filter_by(id = 1).first()
        db.session.delete(tripMaster)

        # queries
        masterInfo = Master.query.filter_by(id=1).all()
        tripInfo = Trips.query.filter_by(Master_Key=1).all()
        particpant_info = Participants.query.filter_by(Master_Key=1).all()
        print(particpant_info)#visual check none of the Jessies sliped through
        particpant_info = Participants.query.filter_by(Master_Key=1).all()

        # Assertions before delete lets make sure everying is the way we want
        self.assertEqual([], masterInfo)  # comparisons
        self.assertEqual([], tripInfo)
        self.assertEqual([], particpant_info)

    def test_expireTrip(self):
        """
        Makes sure that expire trip does the fallowing:
            Deletes trips that have expired
            Deletes associated particpants
            Leaves correct trips
            Leaves correct particpants
        """
        model = TripModel(Inputs['CorrecttestInputRedRocks'])
        model.master.Departure_Date = datetime.date.today() + datetime.timedelta(days=2)

        # add to db
        db.session.add(model.master)
        db.session.add(model.trip)
        db.session.add(model.leader)

        Expiredmodel = TripModel(Inputs['CorrecttestInputRedRocks'])

        # add to db
        db.session.add(Expiredmodel.master)
        db.session.add(Expiredmodel.trip)
        db.session.add(Expiredmodel.leader)

        # make sure both trips were added
        self.assertTrue(len(Master.query.all()) == 2)

        masterInfo = Master.query.checkTrip().all()[0].__dict__

        self.assertTrue(len(Master.query.all()) == 1)

        # masterInfo = Master.query.filter_by(id=1).all()[0].__dict__
        tripInfo = Trips.query.filter_by(Master_Key=1).all()[0].__dict__
        particpant_info = Participants.query.filter_by(Master_Key=1).all()[0].__dict__

        # remove unessary stuff for comparisons
        masterInfo.pop('_sa_instance_state', None)
        tripInfo.pop('_sa_instance_state', None)
        particpant_info.pop('_sa_instance_state', None)
        tripInfo['Weather_Forecast'] = ""  # Take out forcast as this is checked in Constructor tests

        expected_master = deepcopy(Expected['expected_master'])
        expected_master['Departure_Date'] = datetime.date.today() + datetime.timedelta(days=2)

        # Assertions
        self.assertDictEqual(expected_master, masterInfo)  # comparisons
        self.assertDictEqual(Expected['expected_particpant'], particpant_info)
        self.assertDictEqual(Expected['expected_trip'], tripInfo)



# class TestDB(unittest.TestCase):

#
#     def test_addParticipant(self):
#         self.db.AddTrip(testInput)
#         self.db.Addparticipant(testParticipant_AJ, 1)
#         expected_particitant = [(2, 1, 'alasdair Johnson', 9193975206, 'aljohnso@students.pitzer.edu', 1, 5), (1, 1, 'Alasdair Johnson', 9193975206, 'aljohnso@students.pitzer.edu', 1, 3)]
#         particpant_info = self.db.cursor.execute('select * from Participants ORDER BY id DESC ').fetchall()
#         print(particpant_info)
#         master_info = self.db.cursor.execute('select Partcipant_cap, Participant_num from Master where id = 1').fetchall()
#         expected_master = [(8, 2)]
#         self.assertEqual(expected_particitant,particpant_info)
#         self.assertEqual(expected_master, master_info)
#     def test_checkTripMany(self):
#         test_master = copy.deepcopy(self.test_master)
#         test_trip = copy.deepcopy(self.test_trip)
#         for i in range(1,30):
#             test_trip.pop()
#             test_trip.append(i)
#             self.db.cursor.execute(self.db.MASTERDBCOMAND, test_master)
#             self.db.cursor.execute(self.db.TRIPSDBCOMAND, test_trip)
#         test_master1 = test_master[:1] + [str(datetime.date.today() + datetime.timedelta(days=2))] + test_master[2:]
#         test_trip.pop()
#         test_trip.append(30)
#         self.db.cursor.execute(self.db.MASTERDBCOMAND, test_master1)
#         self.db.cursor.execute(self.db.TRIPSDBCOMAND, test_trip)
#         self.db.connection.commit()
#
#         masterInfo = self.db.checkTrip()
#
#         tripInfo = self.db.cursor.execute(
#             'select id, Master_Key, Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone,' \
#             ' Gear_List, Trip_Meeting_Place, Additional_Costs, Total_Cost, Cost_BreakDown, Car_Cap,  ' \
#             'Substance_Frre from Trips order by id desc').fetchall()
#         # print('DB info after check')
#         # print(masterInfo)
#         # print(tripInfo)
#         ExpectedMaster = [(30, 'Red Rocks', str(datetime.date.today() + datetime.timedelta(days=2)), '2016-12-12',
#                            'Turn up ...', str(datetime.date.today()), 1, 2, 'Red Rocks')]  # expected outputs
#         ExpectedTrip = [(30, 30, 'Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', 9193975206,
#                          'All the things', 'Service Road', 10, 95, 'cash for strip club', 5, 0)]
#         self.db.deleteTrip(30)
#         self.assertEqual(ExpectedMaster, masterInfo)  # comparisons
#         self.assertEqual(tripInfo, ExpectedTrip)





    # consider adding waitlist fetures new table?
    # also add email notifiactions confirming particpants
    # add blacklist feature
    #encrypt database files


if __name__ == '__main__':
    unittest.main()
