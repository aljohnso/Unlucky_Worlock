from flask import Flask, g
import os
from DatabaseConnection.DataBaseSchema import db
from Pitzer_Outdoor_Adventure.Main.controllers import main

from flask_bootstrap import Bootstrap
from Config.config import configure_app


app = Flask(__name__)
configure_app(app, 'default')#set app congif here
print("app config set")
Bootstrap(app)
db.init_app(app)
with app.app_context():
    db.create_all()
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.db_session.remove()

app.register_blueprint(main)
print(app.url_map)

