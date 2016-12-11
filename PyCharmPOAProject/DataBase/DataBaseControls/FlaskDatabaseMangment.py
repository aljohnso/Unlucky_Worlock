
import sqlite3
#TODO create functions that create the SQLite calls that fill in database from the forms ie calculate additonal info geo location weather and costs
#TODO get shota to write tests for all of this
def AddTrip():
    """'
    used to construct the db insert for the trip table
    :param
    :return: List of info for table
    """
    Master = []
    Trip = []
    Participants = []
    return Master, Trip, Participants

# app = Flask(__name__)

# wont work becuese DATABASE is configed in our app Im sure there is a work around but I am under time pressuere rn
# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
#
# # Calls connect DB
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
#
# def init_db():
#     """
#     will go to the schema flile
#     :return: VOID
#     """
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
#
# def show_entries(SQL):
#     """
#     Example show_entries('select title, text from entries order by id desc')
#     :param SQL: SQL code that will call table info to be returned
#     :return: entries form sql table look up
#     """
#     db = get_db()
#     cur = db.execute(SQL)
#     entries = cur.fetchall()
#     return entries