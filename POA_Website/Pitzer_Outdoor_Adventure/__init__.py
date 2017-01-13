from flask import Flask
from Pitzer_Outdoor_Adventure.Main.controllers import main
app = Flask(__name__)
from flask_bootstrap import Bootstrap
Bootstrap(app)
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


app.register_blueprint(main)
print(app.url_map)
