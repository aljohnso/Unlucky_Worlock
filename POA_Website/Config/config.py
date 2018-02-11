import uuid, os, json
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # sqlite :memory: identifier is the default if no filepath is present
    try:
        #Here We attempt to load from the AWS RDS DB
        filePath = os.getcwd() + "/secret/databaseURI.json break this code"
        with open(filePath) as data_file:
            data = json.load(data_file)
        SQLALCHEMY_DATABASE_URI = data["SQLALCHEMY_DATABASE_URI"]
        print(SQLALCHEMY_DATABASE_URI)
        data["thisIsmenttoBreak"] += "breakMe"
    except:
        print('WARNING LOCAL DB IN USE AAAAAAAAAĀ')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + '/database/SQLAlchameyPOA.db'
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
    "default": "Config.config.BaseConfig"
}

def configure_app(app, config_name ):
    app.config.from_object(config[config_name])

