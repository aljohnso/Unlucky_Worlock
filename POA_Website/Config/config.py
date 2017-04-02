import uuid, os
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # sqlite :memory: identifier is the default if no filepath is present
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/SQLAlchameyPOA.db'
    SECRET_KEY = str(uuid.uuid4())



class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/SQLAlchameyPOA.db'
    SECRET_KEY = 'dev'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/SQLAlchameyPOA.db'
    SECRET_KEY = 'test'


config = {
    "development": "Config.config.DevelopmentConfig",
    "testing": "Config.config.TestingConfig",
    "default": "Config.config.DevelopmentConfig"
}

def configure_app(app, config_name ):
    app.config.from_object(config[config_name])

