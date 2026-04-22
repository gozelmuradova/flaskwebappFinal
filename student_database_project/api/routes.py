# TeamM2
from flask import Blueprint, jsonify, request
import db

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/students', methods=['GET'])
def get_all_students():
    students = db.get_all_students()
    return jsonify([dict(s) for s in students]), 200

@api_blueprint.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = db.get_student_by_id(student_id)
    if student is None:
        return jsonify({'error': f'Student {student_id} not found.'}), 404
    return jsonify(dict(student)), 200

@api_blueprint.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400
    db.create_student(data['first_name'], data['last_name'],
                      data['email'], data['major'], data['classification'])
    return jsonify({'message': 'Student created successfully.'}), 201

@api_blueprint.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = db.get_student_by_id(student_id)
    if student is None:
        return jsonify({'error': f'Student {student_id} not found.'}), 404
    data = request.get_json()
    db.update_student(student_id, data['first_name'], data['last_name'],
                      data['email'], data['major'], data['classification'])
    return jsonify({'message': 'Student updated successfully.'}), 200

@api_blueprint.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = db.get_student_by_id(student_id)
    if student is None:
        return jsonify({'error': f'Student {student_id} not found.'}), 404
    db.delete_student(student_id)
    return jsonify({'message': 'Student deleted successfully.'}), 200