from DatabaseConnection.DatabaseConnection import *
import os

try:
    db = DatabaseConnection('/var/www/Unlucky_Worlock/POA_Website' + '/bin/POA.db')
except:
    db = DatabaseConnection(os.getcwd() + '/bin/POA.db')
