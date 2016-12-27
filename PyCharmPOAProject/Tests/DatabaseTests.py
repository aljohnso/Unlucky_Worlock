from DatabaseConnection.DataBaseControls.FlaskDatabaseMangment import AddTrip, MASTERDBCOMAND,PARTICIPANTDBCOMAND,TRIPSDBCOMAND
from  DatabaseConnection.DatabaseConnection import DatabaseConnection
import sqlite3, unittest, os, datetime

testInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206, 'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10, 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club', 'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 5, 'Substance_Free': False, 'Trip_Location': 'Red Rocks', 'Departure_Date': datetime.date(2016, 10, 12), 'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'California'}
# conn = sqlite3.connect(str(os.getcwd()) + '/DataBase_Test_Scripts/POA_Test.db')


class TestDB(unittest.TestCase):
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
        masterInfo = self.db.cursor.execute('select id, Trip_Name , Deparure_Date, Return_Date, Details_Short, Participant_num, Partcipant_cap, Trip_Location from  Master WHERE id = 1').fetchall()
        tripInfo = self.db.cursor.execute('select id, Master_Key, Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone, Gear_List, Trip_Meeting_Place, Additional_Costs, Total_Cost, Cost_BreakDown, Car_Cap,  Substance_Frre from  Trips WHERE Master_Key = 1').fetchall()
        ExpectedMaster = [(1, 'Red Rocks', '2016-10-12', '2016-12-12', 'Turn up ...', 1, 2, 'Red Rocks')]
        ExpectedTrip = [(1, 1, 'Turn up and climb', 'Alasdair Johnson', 'aljohnso@students.pitzer.edu', 9193975206, 'All the things','Service Road', 10, 95, 'cash for strip club', 5, 0)]
        self.assertEqual(ExpectedMaster, masterInfo)
        self.assertEqual(tripInfo, ExpectedTrip)

    def deleteTrip(self):
        pass

    def expireTrip(self):
        pass

    def addParticipant(self):
        pass

    def deleteParticipant(self):
        pass

    # consider adding waitlist fetures new table?
    # also add email notifiactions confirming particpants
    # add blacklist feature

if __name__ == '__main__':
    unittest.main()
