from flask import Blueprint, request, jsonify
from flask_module.models import db, Chatlog

bp = Blueprint('chatlog', __name__, url_prefix='/chatlog')

@bp.route('/', methods=['POST'])
def create_chatlog():
    data = request.json
    new_chat = Chatlog(sentBy=data['sentBy'], message=data['message'])
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({'message': 'Chat log created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_chatlogs():
    chats = Chatlog.query.all()
    return jsonify([{'time': c.time, 'sentBy': c.sentBy, 'message': c.message} for c in chats]), 200

# Additional routes for updating and deleting chatlogs can be added similarly to preferences_controller.py
