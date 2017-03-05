from flask import  request, redirect, url_for, \
     render_template, flash,Blueprint
from DatabaseConnection.DataBaseSchema import Master, db
import datetime
main = Blueprint('main', __name__, template_folder='templates')


@main.route('/', methods=['GET', 'POST'])
def Main():
    expected_master = {'Details': 'Turn up and climb', 'Departure_Date': datetime.date.today(),
                       'Post_Time': datetime.date.today(),
                       'Trip_Name': 'Red Rocks', 'Participant_num': 1, 'Return_Date': datetime.date.today(),
                       'Car_Capacity': 3, 'Trip_Location': 'National Conservation Area, Las Vegas, NV'}
    test = Master(expected_master)
    print(test)
    db.session.add(test)
    data = Master.query.all()
    print(data)
    return data[0].Trip_Name 
