import os
import sys

sys.path.insert(0, '/opt/python/current/app/POA_Website/')#production path

from Pitzer_Outdoor_Adventure import app

if __name__ == '__main__':
    app.run()