from DatabaseConnection.DatabaseQuery import *
import os

try:
    db = POA_db_query('/var/www/Unlucky_Worlock/POA_Website' + '/bin/POA.db')
except:
    db = POA_db_query(os.getcwd() + '/bin/POA.db')
