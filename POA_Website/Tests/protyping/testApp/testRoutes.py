from flask import request, redirect, url_for, render_template, flash, Blueprint

from Tests.TestForms.SecondForms import CreateAccountForm
from Tests.protyping.UserAccounts import db, Account, databaseName, currentPath, createAccount
from Tests.protyping.testApp.DatabaseInterfacetest import DatabaseTest

import json

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
    # testInput = {'Trip_Meeting_Place': 'Service Road', 'GearList': 'All the things', 'Coordinator_Phone': 9193975206,
    #              'Car_Capacity': 3, 'Return_Date': datetime.date(2016, 12, 12), 'Additional_Cost': 10,
    #              'Coordinator_Email': 'aljohnso@students.pitzer.edu', 'Cost_Breakdown': 'cash for strip club',
    #              'submit': True, 'Details': 'Turn up and climb', 'Car_Cap': 3, 'Substance_Free': False,
    #              'Trip_Location': 'National Conservation Area, Las Vegas',
    #              'Departure_Date': datetime.date(2016, 10, 12),
    #              'Coordinator_Name': 'Alasdair Johnson', 'Trip_Name': 'Red Rocks', 'Trip_State': 'NV'}
    #
    # response = dataBase.addMaster(testInput)
    # return response[0].Trip_Name
    #http://stackoverflow.com/questions/23712986/pre-populate-a-wtforms-in-flask-with-data-from-a-sqlalchemy-object
    sampleData = {
        'family_name' : 'Vonallmen',
        'locale' : 'en',
        'name' : 'Matthew Vonallmen',
        'picture' : 'badmeme.jpg',
        'given_name' : 'Matthew',
        'id' : '123456789'
    }
    userInfo = json.dumps(sampleData)
    unpackedInfo = json.loads(userInfo)
    form = CreateAccountForm(FirstName_Box = unpackedInfo["given_name"][:], LastName_Box = unpackedInfo["family_name"][:]) # Make this user info.
    if request.method == 'POST':
        # print(form.data)  # returns a dictionary with keys that are the fields in the table
        if form.validate_on_submit() == False:
            flash('All fields are required.')
            return render_template("ModifyAccount.html", form=form)
        else:
            flash('New entry was successfully posted')
            print(form.data)
            unpackedInfo = {
                'family_name': form.data["LastName_Box"],
                'locale': 'en',
                'name': str(form.data["FirstName_Box"][:] + form.data["LastName_Box"][:]),
                'picture': 'badmeme.jpg',
                'given_name': form.data["FirstName_Box"][:],
                'id': '123456789'
            }
            #unpackedInfo = form.data["FirstName_Box"]
            packedInfo = json.dumps(unpackedInfo)
            # First Pass form to class that parse to dict that can be passed to createAccount
            # create the createAcount object and add it to the session then commit
            #EXTRA CREDIT make a page to edit account info
            createAccount(packedInfo)
            #temp = createAccount(packedInfo)
            #temp = Account(form.data['Sample_Box'], "spam", 10000)
            #db.session.add(temp)
            #db.session.commit()
            print(Account.query.all)
            return redirect(url_for('main.postData'))
    elif request.method == 'GET':
        return render_template("ModifyAccount.html", form=form)



@main.route('/data')
def postData():
    a = Account.query.all()
    b =""
    for obj in a:
        b += obj.firstName + " "
    return b

    response = dataBase.addMaster(testInput)
    return response[0].Trip_Name



@main.route("/send")
def index():
    msg = Message("Hello",
                  sender="from@example.com",
                  recipients=["aljohnso@students.pitzer.edu"])
    mail.send(msg)
    return "sent"

