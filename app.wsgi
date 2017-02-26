import os, sys

PROJECT_DIR = '/var/www/Unlucky_Worlock/POA_Website'
VIRTUAL_ENV = "/home/ubuntu"
sys.path.insert(0, PROJECT_DIR)


def execfile(filename):
    globals = dict( __file__ = filename )
    exec( open(filename).read(), globals )

activate_this = os.path.join( VIRTUAL_ENV, 'venv3/bin', 'activate_this.py' )
execfile( activate_this )

# run points to the home.py file
from run import app as application
application.secret_key = "somesecretsessionkey"