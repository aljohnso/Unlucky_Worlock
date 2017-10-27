from flask import Flask
from flask_bootstrap import Bootstrap
import os
from Config.config import configure_app
from DatabaseConnection.DataBaseSchema import db
from Pitzer_Outdoor_Adventure.Main.controllers import main
from Pitzer_Outdoor_Adventure.api.controllers import api, mail
from Pitzer_Outdoor_Adventure.admin.controllers import admin

from flask_mail import Mail

app = Flask(__name__)
configure_app(app, 'default')#set app congif here
Bootstrap(app)
db.init_app(app)
with app.app_context():
   db.create_all()
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.db_session.remove()

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    MAIL_SERVER= 'smtp.gmail.com',
    MAIL_PORT= 465,#587,
    MAIL_USE_TLS= False,
    MAIL_USE_SSL= True,
    MAIL_USERNAME= 'pzgearcloset@gmail.com',
    MAIL_PASSWORD= 'The clearest way into the Universe is through a forest wilderness'
    # MAIL_PASSWORD= 'In every walk with nature one receives far more than he seeks'
))
mail.init_app(app)

app.register_blueprint(main)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(admin, url_prefix="/admin")
print(app.url_map)