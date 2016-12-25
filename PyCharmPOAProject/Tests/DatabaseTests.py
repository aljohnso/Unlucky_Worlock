from DataBase.DataBaseControls.FlaskDatabaseMangment import AddTrip, MASTERDBCOMAND,PARTICIPANTDBCOMAND,TRIPSDBCOMAND
import sqlite3, unittest, os

testInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206, 'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10, 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club', 'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 5, 'Substance_Free': False, 'Trip_Location': 'Red Rocks', 'Departure_Date': datetime.date(2016, 10, 12), 'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'California'}
conn = sqlite3.connect(str(os.getcwd()) + '\\DataBase_Test_Scripts\\POA_Test.db')


class TestDB(unittest.TestCase):

    def setUp(self):
        db = conn.cursor()
        table_commands = open(str(os.getcwd())+'\\DataBase_Test_Scripts\\DataBaseTest_Scripts_CreateTables.sql').read()
        print(table_commands)
        db.executescript(table_commands)
        print("Done")

    def tearDown(self):
        conn.close()

    def addTrip(self):
        db = conn.cursor()
        AddTrip(testInput,db)

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
