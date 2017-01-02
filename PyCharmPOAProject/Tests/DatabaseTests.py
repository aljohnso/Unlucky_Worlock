from  DatabaseConnection.DatabaseConnection import DatabaseConnection
import sqlite3, unittest, os, datetime
import copy
from DatabaseConnection.DatabaseSubmissionConstructors import TripCommandConstructor, MasterCommandConstructor, ParticipantCommandConstructor
testParticipant_AJ = {'Participant':"alasdair Johnson",'Phone': 9193975206, 'Driver': 1, 'Car_Capacity' : 5}
testParticipant_JL = {'Participant':"Jessie Levine",'Phone': 2523456439, 'Driver': 0, 'Car_Capacity' : 0}

testInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206, 'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10, 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club', 'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 5, 'Substance_Free': False, 'Trip_Location': 'Red Rocks', 'Departure_Date': datetime.date(2016, 10, 12), 'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'California'}
# conn = sqlite3.connect(str(os.getcwd()) + '/DataBase_Test_Scripts/POA_Test.db')




class TestDB(unittest.TestCase):
    test_master = ['Red Rocks', '2016-10-12', '2016-12-12', 'Red Rocks', 'Turn up ...', str(datetime.date.today()), 1, 2]
    test_trip = ['Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', '9193975206',
                 'All the things', 'Service Road', '10', 'cash for strip club', '5', 0, 95.0,
                 "{'forecastday': [{'avehumidity': 69, 'qpf_night': {'in': 0.0, 'mm': 0}, 'skyicon': '', 'qpf_day': {'in': None, 'mm': None}, 'qpf_allday': {'in': 0.0, 'mm': 0}, 'low': {'celsius': '-2', 'fahrenheit': '29'}, 'minhumidity': 0, 'icon': 'partlycloudy', 'snow_day': {'cm': None, 'in': None}, 'pop': 20, 'high': {'celsius': '6', 'fahrenheit': '43'}, 'conditions': 'Partly Cloudy', 'date': {'tz_long': 'America/New_York', 'monthname': 'December', 'year': 2016, 'month': 12, 'day': 29, 'sec': 0, 'epoch': '1483056000', 'isdst': '0', 'weekday_short': 'Thu', 'min': '00', 'weekday': 'Thursday', 'monthname_short': 'Dec', 'yday': 363, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on December 29, 2016', 'tz_short': 'EST'}, 'maxwind': {'degrees': 0, 'mph': 0, 'kph': 0, 'dir': ''}, 'avewind': {'degrees': 234, 'mph': 3, 'kph': 5, 'dir': 'SW'}, 'snow_night': {'cm': 0.0, 'in': 0.0}, 'snow_allday': {'cm': 0.0, 'in': 0.0}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/partlycloudy.gif', 'period': 1}, {'avehumidity': 60, 'qpf_night': {'in': 0.0, 'mm': 0}, 'skyicon': '', 'qpf_day': {'in': 0.0, 'mm': 0}, 'qpf_allday': {'in': 0.0, 'mm': 0}, 'low': {'celsius': '-5', 'fahrenheit': '23'}, 'minhumidity': 0, 'icon': 'mostlycloudy', 'snow_day': {'cm': 0.0, 'in': 0.0}, 'pop': 20, 'high': {'celsius': '1', 'fahrenheit': '34'}, 'conditions': 'Mostly Cloudy', 'date': {'tz_long': 'America/New_York', 'monthname': 'December', 'year': 2016, 'month': 12, 'day': 30, 'sec': 0, 'epoch': '1483142400', 'isdst': '0', 'weekday_short': 'Fri', 'min': '00', 'weekday': 'Friday', 'monthname_short': 'Dec', 'yday': 364, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on December 30, 2016', 'tz_short': 'EST'}, 'maxwind': {'degrees': 282, 'mph': 25, 'kph': 40, 'dir': 'WNW'}, 'avewind': {'degrees': 282, 'mph': 18, 'kph': 29, 'dir': 'WNW'}, 'snow_night': {'cm': 0.0, 'in': 0.0}, 'snow_allday': {'cm': 0.0, 'in': 0.0}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/mostlycloudy.gif', 'period': 2}, {'avehumidity': 56, 'qpf_night': {'in': 0.01, 'mm': 0}, 'skyicon': '', 'qpf_day': {'in': 0.02, 'mm': 1}, 'qpf_allday': {'in': 0.03, 'mm': 1}, 'low': {'celsius': '1', 'fahrenheit': '33'}, 'minhumidity': 0, 'icon': 'chancerain', 'snow_day': {'cm': 0.0, 'in': 0.0}, 'pop': 40, 'high': {'celsius': '4', 'fahrenheit': '39'}, 'conditions': 'Chance of Rain', 'date': {'tz_long': 'America/New_York', 'monthname': 'December', 'year': 2016, 'month': 12, 'day': 31, 'sec': 0, 'epoch': '1483228800', 'isdst': '0', 'weekday_short': 'Sat', 'min': '00', 'weekday': 'Saturday', 'monthname_short': 'Dec', 'yday': 365, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on December 31, 2016', 'tz_short': 'EST'}, 'maxwind': {'degrees': 197, 'mph': 15, 'kph': 24, 'dir': 'SSW'}, 'avewind': {'degrees': 197, 'mph': 11, 'kph': 18, 'dir': 'SSW'}, 'snow_night': {'cm': 0.0, 'in': 0.0}, 'snow_allday': {'cm': 0.0, 'in': 0.0}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/chancerain.gif', 'period': 3}, {'avehumidity': 69, 'qpf_night': {'in': 0.14, 'mm': 4}, 'skyicon': '', 'qpf_day': {'in': 0.0, 'mm': 0}, 'qpf_allday': {'in': 0.14, 'mm': 4}, 'low': {'celsius': '1', 'fahrenheit': '33'}, 'minhumidity': 0, 'icon': 'partlycloudy', 'snow_day': {'cm': 0.0, 'in': 0.0}, 'pop': 10, 'high': {'celsius': '5', 'fahrenheit': '41'}, 'conditions': 'Partly Cloudy', 'date': {'tz_long': 'America/New_York', 'monthname': 'January', 'year': 2017, 'month': 1, 'day': 1, 'sec': 0, 'epoch': '1483315200', 'isdst': '0', 'weekday_short': 'Sun', 'min': '00', 'weekday': 'Sunday', 'monthname_short': 'Jan', 'yday': 0, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on January 01, 2017', 'tz_short': 'EST'}, 'maxwind': {'degrees': 263, 'mph': 5, 'kph': 8, 'dir': 'W'}, 'avewind': {'degrees': 263, 'mph': 4, 'kph': 6, 'dir': 'W'}, 'snow_night': {'cm': 0.0, 'in': 0.0}, 'snow_allday': {'cm': 0.0, 'in': 0.0}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/partlycloudy.gif', 'period': 4}, {'avehumidity': 85, 'qpf_night': {'in': 0.41, 'mm': 10}, 'skyicon': '', 'qpf_day': {'in': 0.04, 'mm': 1}, 'qpf_allday': {'in': 0.45, 'mm': 11}, 'low': {'celsius': '4', 'fahrenheit': '40'}, 'minhumidity': 0, 'icon': 'chancerain', 'snow_day': {'cm': 0.0, 'in': 0.0}, 'pop': 60, 'high': {'celsius': '6', 'fahrenheit': '42'}, 'conditions': 'Chance of Rain', 'date': {'tz_long': 'America/New_York', 'monthname': 'January', 'year': 2017, 'month': 1, 'day': 2, 'sec': 0, 'epoch': '1483401600', 'isdst': '0', 'weekday_short': 'Mon', 'min': '00', 'weekday': 'Monday', 'monthname_short': 'Jan', 'yday': 1, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on January 02, 2017', 'tz_short': 'EST'}, 'maxwind': {'degrees': 124, 'mph': 10, 'kph': 16, 'dir': 'SE'}, 'avewind': {'degrees': 124, 'mph': 6, 'kph': 10, 'dir': 'SE'}, 'snow_night': {'cm': 0.0, 'in': 0.0}, 'snow_allday': {'cm': 0.0, 'in': 0.0}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/chancerain.gif', 'period': 5}, {'avehumidity': 90, 'qpf_night': {'in': 0.0, 'mm': 0}, 'skyicon': '', 'qpf_day': {'in': 0.11, 'mm': 3}, 'qpf_allday': {'in': 0.11, 'mm': 3}, 'low': {'celsius': '8', 'fahrenheit': '46'}, 'minhumidity': 0, 'icon': 'rain', 'snow_day': {'cm': 0.0, 'in': 0.0}, 'pop': 90, 'high': {'celsius': '11', 'fahrenheit': '51'}, 'conditions': 'Rain', 'date': {'tz_long': 'America/New_York', 'monthname': 'January', 'year': 2017, 'month': 1, 'day': 3, 'sec': 0, 'epoch': '1483488000', 'isdst': '0', 'weekday_short': 'Tue', 'min': '00', 'weekday': 'Tuesday', 'monthname_short': 'Jan', 'yday': 2, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on January 03, 2017', 'tz_short': 'EST'}, 'maxwind': {'degrees': 203, 'mph': 5, 'kph': 8, 'dir': 'SSW'}, 'avewind': {'degrees': 203, 'mph': 4, 'kph': 6, 'dir': 'SSW'}, 'snow_night': {'cm': 0.0, 'in': 0.0}, 'snow_allday': {'cm': 0.0, 'in': 0.0}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/rain.gif', 'period': 6}, {'avehumidity': 68, 'qpf_night': {'in': 0.0, 'mm': 0}, 'skyicon': '', 'qpf_day': {'in': 0.0, 'mm': 0}, 'qpf_allday': {'in': 0.0, 'mm': 0}, 'low': {'celsius': '-1', 'fahrenheit': '30'}, 'minhumidity': 0, 'icon': 'partlycloudy', 'snow_day': {'cm': 0.0, 'in': 0.0}, 'pop': 20, 'high': {'celsius': '8', 'fahrenheit': '47'}, 'conditions': 'Partly Cloudy', 'date': {'tz_long': 'America/New_York', 'monthname': 'January', 'year': 2017, 'month': 1, 'day': 4, 'sec': 0, 'epoch': '1483574400', 'isdst': '0', 'weekday_short': 'Wed', 'min': '00', 'weekday': 'Wednesday', 'monthname_short': 'Jan', 'yday': 3, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on January 04, 2017', 'tz_short': 'EST'}, 'maxwind': {'degrees': 273, 'mph': 15, 'kph': 24, 'dir': 'W'}, 'avewind': {'degrees': 273, 'mph': 10, 'kph': 16, 'dir': 'W'}, 'snow_night': {'cm': 0.0, 'in': 0.0}, 'snow_allday': {'cm': 0.0, 'in': 0.0}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/partlycloudy.gif', 'period': 7}, {'avehumidity': 52, 'qpf_night': {'in': 0.08, 'mm': 2}, 'skyicon': '', 'qpf_day': {'in': 0.0, 'mm': 0}, 'qpf_allday': {'in': 0.08, 'mm': 2}, 'low': {'celsius': '-4', 'fahrenheit': '24'}, 'minhumidity': 0, 'icon': 'mostlycloudy', 'snow_day': {'cm': 0.0, 'in': 0.0}, 'pop': 0, 'high': {'celsius': '0', 'fahrenheit': '32'}, 'conditions': 'Mostly Cloudy', 'date': {'tz_long': 'America/New_York', 'monthname': 'January', 'year': 2017, 'month': 1, 'day': 5, 'sec': 0, 'epoch': '1483660800', 'isdst': '0', 'weekday_short': 'Thu', 'min': '00', 'weekday': 'Thursday', 'monthname_short': 'Jan', 'yday': 4, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on January 05, 2017', 'tz_short': 'EST'}, 'maxwind': {'degrees': 289, 'mph': 15, 'kph': 24, 'dir': 'WNW'}, 'avewind': {'degrees': 289, 'mph': 11, 'kph': 18, 'dir': 'WNW'}, 'snow_night': {'cm': 2.0, 'in': 0.8}, 'snow_allday': {'cm': 2.0, 'in': 0.8}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/mostlycloudy.gif', 'period': 8}, {'avehumidity': 52, 'qpf_night': {'in': 0.06, 'mm': 2}, 'skyicon': '', 'qpf_day': {'in': 0.09, 'mm': 2}, 'qpf_allday': {'in': 0.16, 'mm': 4}, 'low': {'celsius': '-7', 'fahrenheit': '20'}, 'minhumidity': 0, 'icon': 'snow', 'snow_day': {'cm': 2.5, 'in': 1.0}, 'pop': 40, 'high': {'celsius': '-2', 'fahrenheit': '29'}, 'conditions': 'Snow Showers', 'date': {'tz_long': 'America/New_York', 'monthname': 'January', 'year': 2017, 'month': 1, 'day': 6, 'sec': 0, 'epoch': '1483747200', 'isdst': '0', 'weekday_short': 'Fri', 'min': '00', 'weekday': 'Friday', 'monthname_short': 'Jan', 'yday': 5, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on January 06, 2017', 'tz_short': 'EST'}, 'maxwind': {'degrees': 273, 'mph': 10, 'kph': 16, 'dir': 'W'}, 'avewind': {'degrees': 273, 'mph': 9, 'kph': 14, 'dir': 'W'}, 'snow_night': {'cm': 1.8, 'in': 0.7}, 'snow_allday': {'cm': 4.3, 'in': 1.7}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/snow.gif', 'period': 9}, {'avehumidity': 61, 'qpf_night': {'in': 0.0, 'mm': 0}, 'skyicon': '', 'qpf_day': {'in': 0.0, 'mm': 0}, 'qpf_allday': {'in': 0.0, 'mm': 0}, 'low': {'celsius': '-7', 'fahrenheit': '19'}, 'minhumidity': 0, 'icon': 'partlycloudy', 'snow_day': {'cm': 0.0, 'in': 0.0}, 'pop': 20, 'high': {'celsius': '-2', 'fahrenheit': '28'}, 'conditions': 'Partly Cloudy', 'date': {'tz_long': 'America/New_York', 'monthname': 'January', 'year': 2017, 'month': 1, 'day': 7, 'sec': 0, 'epoch': '1483833600', 'isdst': '0', 'weekday_short': 'Sat', 'min': '00', 'weekday': 'Saturday', 'monthname_short': 'Jan', 'yday': 6, 'hour': 19, 'ampm': 'PM', 'pretty': '7:00 PM EST on January 07, 2017', 'tz_short': 'EST'}, 'maxwind': {'degrees': 278, 'mph': 10, 'kph': 16, 'dir': 'W'}, 'avewind': {'degrees': 278, 'mph': 8, 'kph': 13, 'dir': 'W'}, 'snow_night': {'cm': 0.0, 'in': 0.0}, 'snow_allday': {'cm': 0.0, 'in': 0.0}, 'maxhumidity': 0, 'icon_url': 'http://icons.wxug.com/i/c/k/partlycloudy.gif', 'period': 10}]}",
                 1]

    GETMASTERTESTDBCOMAND = 'select id, Trip_Name , Deparure_Date, Return_Date, Details_Short, Participant_num,' \
                            ' Partcipant_cap, Trip_Location from  Master WHERE id ='
    GETTRIPTESTDBCOMAND = 'select id, Master_Key, Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone,' \
                          ' Gear_List, Trip_Meeting_Place, Additional_Costs, Total_Cost, Cost_BreakDown, Car_Cap,  ' \
                          'Substance_Frre from  Trips WHERE Master_Key ='

    def setUp(self):
        self.db = DatabaseConnection(str(os.getcwd()) + '/DataBase_Test_Scripts/POA_Test.db')
        table_commands = open(str(os.getcwd())+'/DataBase_Test_Scripts/DataBaseTest_Scripts_CreateTables.sql').read()
        self.db.cursor.executescript(table_commands)

    def tearDown(self):
        self.db.closeConnection()

    def test_addTrip(self):
        self.db.AddTrip(testInput)
        masterInfo = self.db.cursor.execute(TestDB.GETMASTERTESTDBCOMAND + '1').fetchall()#will get the info from the line the command calls as a list of tuples where each tuple has the row from the database
        tripInfo = self.db.cursor.execute(TestDB.GETTRIPTESTDBCOMAND + '1').fetchall()
        ExpectedMaster = [(1, 'Red Rocks', '2016-10-12', '2016-12-12', 'Turn up and climb', 1, 2, 'Red Rocks, California')]#expected outputs
        ExpectedTrip = [(1, 1, 'Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', 9193975206,
                         'All the things','Service Road', 10, 180, 'cash for strip club', 5, 0)]
        self.db.deleteTrip(1)
        self.assertEqual(ExpectedMaster, masterInfo)#comparisons
        self.assertEqual(tripInfo, ExpectedTrip)


    def test_deleteTrip(self):
        self.db.AddTrip(testInput)
        self.db.AddTrip(testInput)
        self.db.deleteTrip(1)
        self.db.deleteTrip(2)
        masterInfo = self.db.cursor.execute(TestDB.GETMASTERTESTDBCOMAND + '2').fetchall()
        tripInfo = self.db.cursor.execute(TestDB.GETTRIPTESTDBCOMAND + '2').fetchall()
        ExpectedMaster = []
        ExpectedTrip = []
        self.assertEqual(ExpectedMaster, masterInfo)
        self.assertEqual(tripInfo, ExpectedTrip)

    def test_expireTrip(self):
        test_master = self.test_master
        test_trip = self.test_trip
        print(test_master)
        print(test_trip)
        self.db.cursor.execute(self.db.MASTERDBCOMAND, test_master)
        self.db.cursor.execute(self.db.TRIPSDBCOMAND, test_trip)
        test_master1 = test_master[:1] + [str(datetime.date.today() + datetime.timedelta(days=2))] + test_master[2:]
        test_master1.pop()
        test_master1.append(2)
        print("later date insert")
        print(test_master1)
        test_trip.pop()
        test_trip.append(2)
        self.db.cursor.execute(self.db.MASTERDBCOMAND, test_master1)
        self.db.cursor.execute(self.db.TRIPSDBCOMAND, test_trip)
        # print('Database cintens before check')
        # print('Trips')
        # print(self.db.cursor.execute('select Details, Master_Key  from Trips order by id DESC ').fetchall())
        # print('Master')
        # print(self.db.cursor.execute('select Deparure_Date, id from Master order by id DESC ').fetchall())
        self.db.connection.commit()
        # self.db.AddTrip(testInput)
        # testInput['Departure_Date'] = datetime.date.today() + datetime.timedelta(days=2)
        # self.db.AddTrip(testInput)
        masterInfo = self.db.checkTrip()
         # = self.db.cursor.execute('select * from  Master order by id desc').fetchall()#will get the info from the line the command calls as a list of tuples where each tuple has the row from the database
        tripInfo = self.db.cursor.execute('select id, Master_Key, Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone,' \
                          ' Gear_List, Trip_Meeting_Place, Additional_Costs, Total_Cost, Cost_BreakDown, Car_Cap,  ' \
                          'Substance_Frre from Trips order by id desc').fetchall()
        # print('DB info after check')
        # print(masterInfo)
        # print(tripInfo)
        ExpectedMaster = [(2, 'Red Rocks', str(datetime.date.today() + datetime.timedelta(days=2)), '2016-12-12', 'Turn up ...',str(datetime.date.today()), 1, 2, 'Red Rocks')]#expected outputs
        ExpectedTrip = [(2, 2, 'Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', 9193975206,
                         'All the things','Service Road', 10, 95, 'cash for strip club', 5, 0)]
        self.db.deleteTrip(2)
        self.assertEqual(ExpectedMaster, masterInfo)#comparisons
        self.assertEqual(tripInfo, ExpectedTrip)

    def test_addParticipant(self):
        self.db.AddTrip(testInput)
        self.db.Addparticipant(testParticipant_AJ, 1)
        expected_particitant = [(1,1,"alasdair Johnson",9193975206,1,5)]
        particpant_info = self.db.cursor.execute('select * from Participants ORDER BY id DESC ').fetchall()
        self.assertEqual(expected_particitant,particpant_info)


    def test_deleteParticipant(self):
        self.db.AddTrip(testInput)
        self.db.Addparticipant(testParticipant_AJ, 1)
        self.db.deleteParticpant(1)
        expected_particitant = []
        particpant_info = self.db.cursor.execute('select * from Participants ORDER BY id DESC ').fetchall()
        self.assertEqual(expected_particitant, particpant_info)


    def test_deleteParticipantWithTrip(self):
        self.db.AddTrip(testInput)
        self.db.Addparticipant(testParticipant_AJ, 1)
        self.db.Addparticipant(testParticipant_JL, 1)
        self.db.deleteTrip(1)
        ExpectedMaster = []
        ExpectedTrip = []
        expected_particitant= []
        masterInfo = self.db.cursor.execute(
            'select * from  Master order by id desc').fetchall()  # will get the info from the line the command calls as a list of tuples where each tuple has the row from the database
        tripInfo = self.db.cursor.execute('select * from  Trips order by id desc').fetchall()
        particpant_info = self.db.cursor.execute('select * from Participants ORDER BY id DESC ').fetchall()
        self.assertEqual(expected_particitant, particpant_info)
        self.assertEqual(ExpectedMaster, masterInfo)#comparisons
        self.assertEqual(tripInfo, ExpectedTrip)
    #
    def test_checkTripMany(self):
        test_master = copy.deepcopy(self.test_master)
        test_trip = copy.deepcopy(self.test_trip)
        for i in range(1,30):
            test_trip.pop()
            test_trip.append(i)
            self.db.cursor.execute(self.db.MASTERDBCOMAND, test_master)
            self.db.cursor.execute(self.db.TRIPSDBCOMAND, test_trip)
        test_master1 = test_master[:1] + [str(datetime.date.today() + datetime.timedelta(days=2))] + test_master[2:]
        test_trip.pop()
        test_trip.append(30)
        self.db.cursor.execute(self.db.MASTERDBCOMAND, test_master1)
        self.db.cursor.execute(self.db.TRIPSDBCOMAND, test_trip)
        self.db.connection.commit()

        masterInfo = self.db.checkTrip()

        tripInfo = self.db.cursor.execute(
            'select id, Master_Key, Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone,' \
            ' Gear_List, Trip_Meeting_Place, Additional_Costs, Total_Cost, Cost_BreakDown, Car_Cap,  ' \
            'Substance_Frre from Trips order by id desc').fetchall()
        print('DB info after check')
        print(masterInfo)
        print(tripInfo)
        ExpectedMaster = [(30, 'Red Rocks', str(datetime.date.today() + datetime.timedelta(days=2)), '2016-12-12',
                           'Turn up ...', str(datetime.date.today()), 1, 2, 'Red Rocks')]  # expected outputs
        ExpectedTrip = [(30, 30, 'Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', 9193975206,
                         'All the things', 'Service Road', 10, 95, 'cash for strip club', 5, 0)]
        self.db.deleteTrip(30)
        self.assertEqual(ExpectedMaster, masterInfo)  # comparisons
        self.assertEqual(tripInfo, ExpectedTrip)

    def test_AddTripWithParticipant(self):
        test_master = copy.deepcopy(self.test_master)
        test_trip = copy.deepcopy(self.test_trip)
        test_trip.pop()
        test_trip.append(1)
        self.db.cursor.execute(self.db.MASTERDBCOMAND, test_master)
        self.db.cursor.execute(self.db.TRIPSDBCOMAND, test_trip)
        particpants = self.db.cursor.execute('select Partcipant_cap, Participant_num from Master WHERE id=1').fetchall()[0]
        print(particpants)
        self.db.Addparticipant(testParticipant_AJ, 1)#driver car cap
        particpants = self.db.cursor.execute('select Partcipant_cap, Participant_num from Master WHERE id=1').fetchall()[0]
        expectedparticpants = (8,2)
        self.assertEqual(particpants,expectedparticpants)





    # consider adding waitlist fetures new table?
    # also add email notifiactions confirming particpants
    # add blacklist feature
    #encrypt database files


if __name__ == '__main__':
    unittest.main()
