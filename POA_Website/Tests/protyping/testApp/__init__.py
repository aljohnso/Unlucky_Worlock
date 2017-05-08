from flask import Flask, g
from Tests.protyping.testApp.testRoutes import main
app = Flask(__name__)
from Tests.protyping.UserAccounts import db
from flask_bootstrap import Bootstrap
import os

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/SQLAlchameyPOA.db'
))
db.init_app(app)
Bootstrap(app)
#wow
with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
    db.create_all()


app.register_blueprint(main)