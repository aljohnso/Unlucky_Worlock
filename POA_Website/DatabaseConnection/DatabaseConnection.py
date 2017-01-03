import sqlite3, requests, datetime
from DatabaseConnection.DatabaseSubmissionConstructors import TripCommandConstructor, MasterCommandConstructor, ParticipantCommandConstructor


class DatabaseConnection:
    """
        This class contains all maniputaltion fuctions for the database by intializing the object we open the database
        Assumes POA Schema 12-26-16
        TODO:CHANGE IF UPDATED

    """
    MASTERDBCOMAND = 'insert into Master (Trip_Name, Deparure_Date,Return_Date,Trip_Location, Details_Short, ' \
                     'Post_Time, Participant_num, Partcipant_cap) VALUES (?,?,?,?,?,?,?,?)'

    TRIPSDBCOMAND = 'insert into Trips (Details, Coordinator_Name, Coordinator_Email, Coordinator_Phone, ' \
                    'Gear_List, Trip_Meeting_Place, Additional_Costs, Cost_BreakDown, Car_Cap, Substance_Frre, ' \
                    'Total_Cost, Weather_Forcast, Master_Key) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'

    PARTICIPANTDBCOMAND = 'insert into Participants (Trips_Key, Participant, Phone, Driver, Car_Capacity)' \
                          ' VALUES (?,?,?,?,?)'

    def __init__(self, path):
        """
            Will create Datbase Connection
        """
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def closeConnection(self):
        self.connection.close()

    def AddTrip(self, form):
        """'
            used to construct the db insert for the trip table
            :param form is the form from POAForms class  MakeTripFormPOA
            :return: List of info for table
        """
        Master = MasterCommandConstructor(form).master
        # print(Master)
        self.cursor.execute(DatabaseConnection.MASTERDBCOMAND, Master)
        Trip = TripCommandConstructor(form,self.cursor.lastrowid).trip
        print(Trip)
        # print(TRIPSDBCOMAND)
        self.cursor.execute(DatabaseConnection.TRIPSDBCOMAND, Trip)
        self.connection.commit()

    def deleteTrip(self, MasterID):
        """
            Will Delete trip from database based on trip ID from Master Table and Trips Table
            :param TripID:
            :return: None
        """

        self.cursor.execute('DELETE FROM Master WHERE id=' + str(MasterID))#wrong
        self.connection.commit()

    def checkTrip(self, server_time = datetime.datetime.now()):
        data = self.cursor.execute('select Deparure_Date, id from  Master order by id desc').fetchall()
        for ENTREE in data:
            departuredate = datetime.datetime.strptime(ENTREE[0], '%Y-%m-%d')
            if server_time >= departuredate:
                self.cursor.execute('DELETE FROM Master WHERE id=' + str(ENTREE[1]))
        self.connection.commit()
        return self.cursor.execute('select * from  Master order by id desc').fetchall()

    def Addparticipant(self, Form, tripID):
        participant = ParticipantCommandConstructor(Form, tripID).participant
        car_capacity = participant[4]
        self.cursor.execute(self.PARTICIPANTDBCOMAND, participant)
        self.cursor.execute('UPDATE Master SET Participant_num = Participant_num + 1 WHERE id =' + str(tripID))#TODO: this could cause an error not sure if trip and master will ever have diffrent ids
        self.cursor.execute('UPDATE Master SET Partcipant_cap = Partcipant_cap +' + str(car_capacity) +' WHERE id =' + str(tripID))
        self.connection.commit()

    def getParticipants(self, tripID):
        try:
            particpants = self.cursor.execute('SELECT * FROM Particpants WHERE Master_Key = ' + tripID)
            return particpants
        except:
            return None

    def deleteParticpant(self, participant_id):
        data = self.cursor.execute('SELECT car_Capacity, Trips_Key FROM Participants WHERE id=' + str(participant_id)).fetchall()
        car_capacity = data[0][0]
        trip_key = data[0][1]
        self.cursor.execute('UPDATE Master SET Participant_num = '
                            'Participant_num - 1 WHERE id =' + str(trip_key))
        self.cursor.execute('UPDATE Master SET Partcipant_cap = Partcipant_cap -'
                            + str(car_capacity) + ' WHERE id =' + str(trip_key))
        self.cursor.execute('DELETE FROM Participants WHERE id=' + str(participant_id))
        self.connection.commit()

    def getTrip(self,Master_Key):
        master_details = self.cursor.execute('select * from Master WHERE id =' + str(Master_Key)).fetchall()
        trip_details = self.cursor.execute('select * from Trips WHERE Master_Key =' + str(Master_Key)).fetchall()
        particpant_details = self.cursor.execute('select Participant, Driver, Car_Capacity, id from Participants '
                                                 'where Trips_Key=' + str(trip_details[0][0])).fetchall()
        return trip_details, master_details, particpant_details









