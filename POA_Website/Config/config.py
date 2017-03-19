import uuid, os
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    SQLALCHEMY_DATABASE_URI = 'sqlite:///~/code/Unlucky_Worlock/POA_Website/Tests/SQLAlchameyPOA.db'
    SECRET_KEY = str(uuid.uuid4())



class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///~/code/Unlucky_Worlock/POA_Website/Tests/SQLAlchameyPOA.db'
    SECRET_KEY = 'dev'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///~/code/Unlucky_Worlock/POA_Website/Tests/SQLAlchameyPOA.db'
    SECRET_KEY = 'test'


config = {
    "development": "Pitzer_Outdoor_Adventure.config.DevelopmentConfig",
    "testing": "Pitzer_Outdoor_Adventure.config.TestingConfig",
    "default": "Pitzer_Outdoor_Adventure..config.DevelopmentConfig"
}

def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])

