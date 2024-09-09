import pytest
import json
from app import app, db
from models import Employee

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

@pytest.fixture
def add_employee():
    """Helper function to add an employee."""
    with app.app_context():
        employee = Employee(
            name='Test User',
            email='test@example.com',
            position='Software Developer',
            salary=50000,
            age=30,
            address='123 Main St, Anytown, 12345',
            skills='Python,Flask'
        )
        db.session.add(employee)
        db.session.commit()
        return employee.id  # Return the employee's ID instead of the instance

# Test adding an employee
def test_add_employee(client):
    data = {
        'name': 'Manan',
        'email': 'manan@example.com',
        'position': 'Software Developer',
        'salary': 80000.0,
        'age': 25,
        'address': {
            'street': '123 Main St',
            'city': 'Anytown',
            'zip': '12345'
        },
        'skills': ['Python', 'Flask', 'Docker']
    }
    response = client.post('/employees', json=data)
    assert response.status_code == 201

# Test retrieving all employees
def test_get_employees(client, add_employee):
    response = client.get('/employees')
    assert response.status_code == 200
    employees = json.loads(response.data)
    assert len(employees) == 1
    assert employees[0]['name'] == 'Test User'

# Test retrieving a specific employee by ID
def test_get_employee(client, add_employee):
    with app.app_context():
        response = client.get(f'/employees/{add_employee}')
        assert response.status_code == 200
        employee_data = json.loads(response.data)
        assert employee_data['name'] == 'Test User'

# Test updating an employee
def test_update_employee(client, add_employee):
    updated_data = {
        "name": "Updated User",
        "email": "updated@example.com",
        "position": "Senior Developer",
        "salary": 70000
    }

    with app.app_context():
        response = client.put(f'/employees/{add_employee}', data=json.dumps(updated_data), content_type='application/json')
        assert response.status_code == 200
        updated_employee = json.loads(response.data)['employee']
        assert updated_employee['name'] == 'Updated User'

# Test deleting an employee
def test_delete_employee(client, add_employee):
    with app.app_context():
        response = client.delete(f'/employees/{add_employee}')
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['message'] == 'Employee deleted successfully'

        # Check that the employee is no longer in the database
        response = client.get(f'/employees/{add_employee}')
        assert response.status_code == 404
