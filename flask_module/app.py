from flask import Flask
from flask_module.models import db
import flask_module.controllers.preferences_controller as preferences
import flask_module.controllers.chatlog_controller as chatlog

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)        
    
    with app.app_context():
        db.create_all()

    from flask_module.controllers.preferences_controller import bp as preferences_bp
    from flask_module.controllers.chatlog_controller import bp as chatlog_bp
    app.register_blueprint(preferences_bp)
    app.register_blueprint(chatlog_bp)

    return app
