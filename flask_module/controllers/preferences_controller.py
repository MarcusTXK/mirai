from flask import Blueprint, request, jsonify
from flask_module.models import db, Preference

bp = Blueprint('preferences', __name__, url_prefix='/preferences')

@bp.route('/', methods=['POST'])
def create_preference():
    data = request.json
    new_pref = Preference(description=data['description'], updatedBy=data['updatedBy'])
    db.session.add(new_pref)
    db.session.commit()
    return jsonify({'message': 'Preference created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_preferences():
    prefs = Preference.query.all()
    return jsonify([{'description': p.description, 'updatedAt': p.updatedAt} for p in prefs]), 200

@bp.route('/<int:id>', methods=['PUT'])
def update_preference(id):
    pref = Preference.query.get_or_404(id)
    data = request.json
    pref.description = data['description']
    pref.updatedBy = data['updatedBy']
    db.session.commit()
    return jsonify({'message': 'Preference updated successfully'}), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_preference(id):
    pref = Preference.query.get_or_404(id)
    db.session.delete(pref)
    db.session.commit()
    return jsonify({'message': 'Preference deleted successfully'}), 200
