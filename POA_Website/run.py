import os
import sys


sys.path.insert(0, '/opt/python/current/app/POA_Website/')#production path

from Pitzer_Outdoor_Adventure import app
sys.path.insert(0,"/var/www/FlaskApps/PlagiarismDefenderApp/")
app.secret_key = "somesecretsessionkey"