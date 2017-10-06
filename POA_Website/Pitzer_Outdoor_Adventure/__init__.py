from flask import Flask
from flask_bootstrap import Bootstrap
import os
from Config.config import configure_app
from DatabaseConnection.DataBaseSchema import db
from Pitzer_Outdoor_Adventure.Main.controllers import main
from Pitzer_Outdoor_Adventure.api.controllers import api


print(os.listdir(os.getcwd()))
app = Flask(__name__)
configure_app(app, 'default')#set app congif here
Bootstrap(app)
db.init_app(app)
#with app.app_context():
 #   db.create_all()
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.db_session.remove()

app.register_blueprint(main)
app.register_blueprint(api, url_prefix="/api")
print(app.url_map)

