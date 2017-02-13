from Flask import Flask, g
from Pitzer_Outdoor_Adventure.Main.controllers import main
app = Flask(__name__)
from flask_bootstrap import Bootstrap
Bootstrap(app)
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.closeConnection()

app.register_blueprint(main)
print(app.url_map)

if __name__ == "__main__":
    app.run()