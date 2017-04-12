from flask import  request, redirect, url_for, \
     render_template, flash,Blueprint
from DatabaseConnection.DataBaseSchema import Master, db
import datetime
from Tests.protyping.testApp.DatabaseInterfacetest import DatabaseTest
from flask_mail import Message, Mail
main = Blueprint('main', __name__, template_folder='templates')

dataBase = DatabaseTest()
mail = Mail()
@main.route('/', methods=['GET', 'POST'])
def Main():
    # expected_master = {'Details': 'Turn up and climb', 'Departure_Date': datetime.date.today(),
    #                    'Post_Time': datetime.date.today(),
    #                    'Trip_Name': 'Red Rocks', 'Participant_num': 1, 'Return_Date': datetime.date.today(),
    #                    'Car_Capacity': 3, 'Trip_Location': 'National Conservation Area, Las Vegas, NV'}
    # test = Master(expected_master)
    # print(test)
    # db.session.add(test)
    # data = Master.query.all()
    # print(data)
    # return data[0].Trip_Name
    testInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206,
                 'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10,
                 'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club',
                 'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 3, 'Substance_Free': False,
                 'Trip_Location': 'National Conservation Area, Las Vegas',
                 'Departure_Date': datetime.date(2016, 10, 12),
                 'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'NV'}

    response = dataBase.addMaster(testInput)
    return response[0].Trip_Name



@main.route("/send")
def index():
    msg = Message("Hello",
                  sender="from@example.com",
                  recipients=["aljohnso@students.pitzer.edu"])
    mail.send(msg)
    return "sent"