# Employee Management API

This project is a RESTful API for managing employee data, built using Flask, SQLAlchemy, and Flasgger for API documentation. The API allows users to create, retrieve, update, and delete employee records.

## Features

- Add, update, delete, and retrieve employee details
- SQLAlchemy as ORM for database interaction
- Unit tests for API endpoints
- Auto-generated API documentation with Flasgger

## Requirements

Make sure you have the following installed:

- Python 3.x
- Flask
- SQLAlchemy
- Flasgger (for API documentation)
- SQLite (for the database)

You can install all required dependencies using `requirements.txt`.

## Setup Instructions

### 1. Clone the repository:

```bash
git clone https://github.com/Manan2506/Employee-Management.git
cd Employee-Management
```

### 2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
# or
venv\Scripts\activate  # For Windows
```
### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database:
You can use SQLite (default) or configure a different database.

For SQLite, run the following commands in Python shell:

```bash
python
```
Then inside the shell:

```
from app import db
db.create_all()
exit()
```

### 5. Run the application:
Start the Flask development server:
```bash
flask run
```

By default, the server will be available at http://127.0.0.1:5000.

### 6. View API Documentation:
Once the app is running, navigate to http://127.0.0.1:5000/apidocs to view the Swagger UI for your API documentation.

## Running Tests

Unit tests are available for the API endpoints. You can run them using pytest.

1. Install pytest if not already installed:

```bash
pip install pytest
```

2. Run the tests:

```bash
pytest
```

## Database Schema

The database is managed using SQLAlchemy ORM. The key model used is Employee, which stores the following fields:

- id: Integer (Primary Key)
- name: String
- email: String (Unique)
- position: String
- salary: Float
- age: Integer
- address: String (JSON)
- skills: String (Comma-separated)

## API Endpoints

### POST /employees

- Add a new employee.

### GET /employees

- Retrieve all employees.

### GET /employees/{id}

- Retrieve a specific employee by ID.

### PUT /employees/{id}

- Update an employee's details.

### DELETE /employees/{id}

- Delete an employee by ID.
