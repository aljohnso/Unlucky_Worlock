from DatabaseConnection.DataBaseControls.FlaskDatabaseMangment import AddTrip, MASTERDBCOMAND,PARTICIPANTDBCOMAND,TRIPSDBCOMAND
from  DatabaseConnection.DatabaseConnection import DatabaseConnection
import sqlite3, unittest, os, datetime

testInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206, 'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10, 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club', 'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 5, 'Substance_Free': False, 'Trip_Location': 'Red Rocks', 'Departure_Date': datetime.date(2016, 10, 12), 'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'California'}
# conn = sqlite3.connect(str(os.getcwd()) + '/DataBase_Test_Scripts/POA_Test.db')


class TestDB(unittest.TestCase):
    GETMASTERTESTDBCOMAND = 'select id, Trip_Name , Deparure_Date, Return_Date, Details_Short, Participant_num,' \
                            ' Partcipant_cap, Trip_Location from  Master WHERE id ='
    GETTRIPTESTDBCOMAND = 'select id, Master_Key, Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone,' \
                          ' Gear_List, Trip_Meeting_Place, Additional_Costs, Total_Cost, Cost_BreakDown, Car_Cap,  ' \
                          'Substance_Frre from  Trips WHERE Master_Key ='

    def setUp(self):
        self.db = DatabaseConnection(str(os.getcwd()) + '/DataBase_Test_Scripts/POA_Test.db')
        table_commands = open(str(os.getcwd())+'/DataBase_Test_Scripts/DataBaseTest_Scripts_CreateTables.sql').read()
        # print(table_commands)
        self.db.cursor.executescript(table_commands)
        print("Done")

    def tearDown(self):
        self.db.closeConnection()

    def test_addTrip(self):
        self.db.AddTrip(testInput)
        masterInfo = self.db.cursor.execute(TestDB.GETMASTERTESTDBCOMAND + '1').fetchall()#will get the info from the line the command calls as a list of tuples where each tuple has the row from the database
        tripInfo = self.db.cursor.execute(TestDB.GETTRIPTESTDBCOMAND + '1').fetchall()
        ExpectedMaster = [(1, 'Red Rocks', '2016-10-12', '2016-12-12', 'Turn up ...', 1, 2, 'Red Rocks')]#expected outputs
        ExpectedTrip = [(1, 1, 'Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', 9193975206,
                         'All the things','Service Road', 10, 95, 'cash for strip club', 5, 0)]
        self.assertEqual(ExpectedMaster, masterInfo)#comparisons
        self.assertEqual(tripInfo, ExpectedTrip)


    def test_deleteTrip(self):
        self.db.AddTrip(testInput)
        self.db.AddTrip(testInput)
        self.db.deleteTrip(2)
        masterInfo = self.db.cursor.execute(TestDB.GETMASTERTESTDBCOMAND + '2').fetchall()
        tripInfo = self.db.cursor.execute(TestDB.GETTRIPTESTDBCOMAND + '2').fetchall()
        ExpectedMaster = []
        ExpectedTrip = []
        self.assertEqual(ExpectedMaster, masterInfo)
        self.assertEqual(tripInfo, ExpectedTrip)

    def test_expireTrip(self):
        self.db.AddTrip(testInput)
        testInput['Departure_Date'] = datetime.date.today() + datetime.timedelta(days=2)
        self.db.AddTrip(testInput)
        self.db.checkTrip()
        masterInfo = self.db.cursor.execute('select * from  Master order by id desc').fetchall()#will get the info from the line the command calls as a list of tuples where each tuple has the row from the database
        tripInfo = self.db.cursor.execute('select id, Master_Key, Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone,' \
                          ' Gear_List, Trip_Meeting_Place, Additional_Costs, Total_Cost, Cost_BreakDown, Car_Cap,  ' \
                          'Substance_Frre from  Trips order by id desc').fetchall()
        ExpectedMaster = [(2, 'Red Rocks', str(datetime.date.today() + datetime.timedelta(days=2)), '2016-12-12', 'Turn up ...',str(datetime.date.today()), 1, 2, 'Red Rocks')]#expected outputs
        ExpectedTrip = [(2, 2, 'Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', 9193975206,
                         'All the things','Service Road', 10, 95, 'cash for strip club', 5, 0)]
        self.assertEqual(ExpectedMaster, masterInfo)#comparisons
        self.assertEqual(tripInfo, ExpectedTrip)

    def test_addParticipant(self):
        pass

    def test_deleteParticipant(self):
        pass

    def test_deleteParticipantWithTrip(self):
        pass
    # consider adding waitlist fetures new table?
    # also add email notifiactions confirming particpants
    # add blacklist feature
    #encrypt database files


if __name__ == '__main__':
    unittest.main()
