import requests
from flask import Blueprint, request, jsonify
from models import db, Employee
from datetime import datetime, timezone
from dateutil import parser

employees_bp = Blueprint('employees', __name__)


# Add a new employee
@employees_bp.route('', methods=['POST'])
def add_employee():
    data = request.get_json()
    try:

        address_data = data.get('address', {})
        street = address_data.get('street')
        city = address_data.get('city')
        zip_code = address_data.get('zip')

        # Create a new employee with the provided details
        employee = Employee(
            name=data['name'],
            email=data['email'],
            position=data['position'],
            salary=data['salary'],
            age=data.get('age'),
            address=f"{street}, {city}, {zip_code}",
            skills=','.join(data.get('skills', []))
        )
        db.session.add(employee)
        db.session.commit()

        # Call external API with structured address
        external_api_payload = {
            "name": employee.name,
            "job": employee.position,
            "email": employee.email,
            "age": employee.age,
            "address": {
                "street": street,
                "city": city,
                "zip": zip_code
            },
            "skills": data.get('skills', [])
        }
        print(external_api_payload)
        response = requests.post(
            "https://reqres.in/api/users",
            json=external_api_payload,
            headers={"Content-Type": "application/json"}
        )
        # import pdb;pdb.set_trace()
        if response.ok:
            response_data = response.json()
            employee.id = response_data.get('id', employee.id)
            created_at_str = response_data.get('createdAt', employee.created_on.isoformat())

            employee.created_on = parser.isoparse(created_at_str)

            if employee.created_on.tzinfo is None:
                employee.created_on = employee.created_on.replace(tzinfo=timezone.utc)

            db.session.commit()

            return jsonify({
                'message': 'Employee created and updated successfully with external API data',
                'employee': employee.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Failed to communicate with external API'}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Retrieve all employees
@employees_bp.route('', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees]), 200


# Retrieve a specific employee by ID
@employees_bp.route('/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify(employee.to_dict()), 200


# Update employee information
@employees_bp.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    data = request.get_json()
    employee.name = data.get('name', employee.name)
    employee.email = data.get('email', employee.email)
    employee.position = data.get('position', employee.position)
    employee.salary = data.get('salary', employee.salary)

    db.session.commit()

    return jsonify({'message': 'Employee updated successfully', 'employee': employee.to_dict()}), 200


# Delete an employee
@employees_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({'message': 'Employee deleted successfully'}), 200
