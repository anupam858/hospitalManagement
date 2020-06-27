from flask import Flask
from flask_mongoengine import MongoEngine
from . import hospitalmanagement
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config= True)
    
    app.config.from_mapping(
    SECRET_KEY='this_is_1hes3cr31key23ncrypt'
    )
    app.config['MONGODB_SETTINGS'] = {
    'db': 'hospital_database'
    }

    db = MongoEngine(app)
    app.register_blueprint(hospitalmanagement.bp)

    return app
