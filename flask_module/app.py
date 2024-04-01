from flask import Flask
from flask_module.models import db
import flask_module.controllers.preferences_controller as preferences
import flask_module.controllers.chatlog_controller as chatlog
import flask_module.controllers.iot_data_controller as iot_data
from flask_cors import CORS 

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)        
    
    with app.app_context():
        db.create_all()
    app.register_blueprint(preferences.bp)
    app.register_blueprint(chatlog.bp)
    app.register_blueprint(iot_data.bp)

    return app
