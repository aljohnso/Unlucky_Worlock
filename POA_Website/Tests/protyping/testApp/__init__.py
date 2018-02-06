from flask import Flask, g
from Tests.protyping.testApp.testRoutes import main, mail
app = Flask(__name__)
from Tests.protyping.UserAccounts import db
from flask_bootstrap import Bootstrap
import os

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/SQLAlchameyPOA.db',
    MAIL_SERVER= 'smtp.gmail.com',
    MAIL_PORT= 587,
    MAIL_USE_TLS= True,
    MAIL_USE_SSL= False,
    MAIL_USERNAME= 'pzgearcloset@gmail.com',
    MAIL_PASSWORD= '',
))
db.init_app(app)
Bootstrap(app)
#wow
from flask_mail import Mail
mail.init_app(app)

with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
    db.create_all()


app.register_blueprint(main)
