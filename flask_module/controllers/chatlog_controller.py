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
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    pagination = Chatlog.query.order_by(Chatlog.time.desc()).paginate(page=page, per_page=size, error_out=False)
    return jsonify({
        'data': [chat.to_dict() for chat in pagination.items],
        'total_pages': pagination.pages,
        }), 200
