from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from flask_module.models import db, IoTData
from datetime import datetime

bp = Blueprint('iot_data', __name__, url_prefix='/iot_data')

@bp.route('/', methods=['POST'])
def create_iot_data():
    data = request.json
    # Convert the time string to a datetime object
    time_str = data.get('time')
    time_obj = datetime.fromisoformat(time_str) if time_str else None

    new_data = IoTData(
        topic=data['topic'],
        unit=data['unit'],
        location=data['location'],
        data=data['data'],
        time=time_obj  # Use the converted datetime object
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'IoT Data created successfully'}), 201

@bp.route('/', methods=['GET'])
def get_iot_data():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    topic_filter = request.args.get('topic', None)

    query = IoTData.query

    if topic_filter:
        # Use the % wildcard to allow for partial matches before and after the topic_filter value
        query = query.filter(IoTData.topic.like(f'%{topic_filter}%'))
    
    # Order by descending time and paginate the query
    pagination = query.order_by(desc(IoTData.time)).paginate(page=page, per_page=size, error_out=False)
    all_data = pagination.items

    return jsonify({
        'data': [d.to_dict() for d in all_data],
        'total_pages': pagination.pages,
        }), 200

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
