from flask import Flask
from employees.routes import employees_bp
from models import db
from config import Config
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yaml')
app.config.from_object(Config)

# Register Blueprint for employees
app.register_blueprint(employees_bp, url_prefix='/employees')

# Initialize the database
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
