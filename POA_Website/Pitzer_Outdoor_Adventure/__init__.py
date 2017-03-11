from flask import Flask, g
import os
from DatabaseConnection.DataBaseSchema import db
from Pitzer_Outdoor_Adventure.Main.controllers import main
app = Flask(__name__)
from flask_bootstrap import Bootstrap
Bootstrap(app)
SQLALCHEMY_DATABASE_URI='sqlite:///' + os.getcwd() + '/SQLAlchameyPOA.db'
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI))
print("app config set")
db.init_app(app)
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.closeConnection()

app.register_blueprint(main)
# print(app.url_map)

