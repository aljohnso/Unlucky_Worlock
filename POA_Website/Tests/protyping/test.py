from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os, datetime
from DatabaseConnection.DataBaseSchema import Master, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.getcwd() + '/SQLAlchameyPOA.db'

db.create_all()


# engine = create_engine('sqlite:///' + os.getcwd() + '/SQLAlchameyPOA.db', convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
# def init_db():
#     import DatabaseConnection.DataBaseSchema
#     Base.metadata.create_all(bind=engine)




expected_master = {'Details': 'Turn up and climb', 'Departure_Date': '2016-10-12', 'Post_Time': str(datetime.date.today()),
         'Trip_Name': 'Red Rocks', 'Participant_num': 1, 'Return_Date': '2016-12-12', 'Car_Capacity': 3,
         'Trip_Location': 'National Conservation Area, Las Vegas, NV'}
test = Master(expected_master)
print(test)
db.session.add(test)
print(Master.query.all())

