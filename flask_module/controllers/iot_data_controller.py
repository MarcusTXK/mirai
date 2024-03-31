from flask import Blueprint, request, jsonify
from flask_module.models import db, IoTData

bp = Blueprint('iot_data', __name__, url_prefix='/iot_data')

@bp.route('/', methods=['POST'])
def create_iot_data():
    data = request.json
    new_data = IoTData(
        topic=data['topic'],
        unit=data['unit'],
        location=data['location'],
        data=data['data']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'IoT Data created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_iot_data():
    all_data = IoTData.query.all()
    return jsonify([
        {
            'topic': d.topic,
            'unit': d.unit,
            'location': d.location,
            'data': d.data,
            'createdAt': d.createdAt
        } for d in all_data
    ]), 200

@bp.route('/<int:id>', methods=['PUT'])
def update_iot_data(id):
    data = IoTData.query.get_or_404(id)
    request_data = request.json
    data.topic = request_data.get('topic', data.topic)
    data.unit = request_data.get('unit', data.unit)
    data.location = request_data.get('location', data.location)
    data.data = request_data.get('data', data.data)
    db.session.commit()
    return jsonify({'message': 'IoT Data updated successfully'}), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_iot_data(id):
    data = IoTData.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return jsonify({'message': 'IoT Data deleted successfully'}), 200
