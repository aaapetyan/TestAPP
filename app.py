from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
# defining the dialect and path to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)
api = Api(app)


# creating the database model
class EmployeesRecord(db.Model):
    last_name = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    father_name = db.Column(db.String(80), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True, unique=True)
    salary = db.Column(db.Float, nullable=False)
    position = db.Column(db.String(80), nullable=False)
    legal_name = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(80), nullable=False)

    # serializing the output
    def serialize(self):
        return {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'father_name': self.father_name,
            'birth_year': self.birth_year,
            'id': self.id,
            'salary': self.salary,
            'position': self.position,
            'legal_name': self.legal_name,
            'department': self.department
        }


# full list of arguments
parser = reqparse.RequestParser()
parser.add_argument('last_name', required=True)
parser.add_argument('first_name', required=True)
parser.add_argument('father_name', required=True)
parser.add_argument('birth_year', type=int, required=True)
parser.add_argument('id', type=int, required=True)
parser.add_argument('salary', type=float, required=True)
parser.add_argument('position', required=True)
parser.add_argument('legal_name', required=True)
parser.add_argument('department', required=True)

# arguments for search by name
search_parser = reqparse.RequestParser()
search_parser.add_argument('last_name', required=True)
search_parser.add_argument('first_name', required=True)
search_parser.add_argument('father_name', required=True)

# correct input data types for a new record
input_types = {'last_name': str, 'first_name': str, 'father_name': str, 'birth_year': int,
               'id': int, 'salary': float, 'position': str, 'legal_name': str, 'department': str}
search_types = {'last_name': str, 'first_name': str, 'father_name': str}


# decorator for validation of input data
def validate(types):
    def decorator(method):
        @wraps(method)
        def wrapper(self):
            # checking if the arguments collected from the request are of the correct type
            for param in types:
                if param not in request.json:
                    return {'error': f'{param} is missing'}
                if types[param] != type(request.json[param]):
                    return {'error': f'{param} should be {types[param]} not {type(request.json[param])}'}
            return method(self)

        return wrapper

    return decorator


# decorator for getting a result or the error
def result_or_error(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return {'result': method(self, *args, **kwargs)}
        except Exception as e:
            return {'error': str(e)}

    return wrapper


class EmployeesRecordList(Resource):
    # to get the full list of employees
    @result_or_error
    def get(self):
        records = EmployeesRecord.query.all()
        return [EmployeesRecord.serialize(record) for record in records]

    # to add a new employee to the list
    @validate(input_types)
    @result_or_error
    def post(self):
        # collecting data from the request
        args = parser.parse_args()
        employee_record = EmployeesRecord(last_name=args['last_name'],
                                          first_name=args['first_name'],
                                          father_name=args['father_name'],
                                          birth_year=args['birth_year'],
                                          id=args['id'],
                                          salary=args['salary'],
                                          position=args['position'],
                                          legal_name=args['legal_name'],
                                          department=args['department'])
        requested_id = args['id']
        # checking if the record with this id already exists
        if EmployeesRecord.query.filter_by(id=requested_id).first() is not None:
            abort(f'Record with id={requested_id} already exists')
        db.session.add(employee_record)
        db.session.commit()
        return EmployeesRecord.serialize(employee_record)


class Employee(Resource):
    # to search for the employee by id
    @result_or_error
    def get(self, emp_id):
        return EmployeesRecord.serialize(
            EmployeesRecord.query.filter_by(id=emp_id).first_or_404
            (description=f'Record with id={emp_id} is not available'))

    # to update the information for the existing employee
    @validate(input_types)
    @result_or_error
    def put(self, emp_id):
        # collecting data from the request
        args = parser.parse_args()
        # finding the record we are going to modify
        record = EmployeesRecord.query.filter_by(id=emp_id) \
            .first_or_404(description=f'Record with id={emp_id} is not available')
        record.last_name = args['last_name']
        record.first_name = args['first_name']
        record.father_name = args['father_name']
        record.birth_year = args['birth_year']
        record.id = args['id']
        record.salary = args['salary']
        record.position = args['position']
        record.legal_name = args['legal_name']
        record.department = args['department']
        db.session.commit()
        return EmployeesRecord.serialize(record)

    # to delete an employee from the list
    @result_or_error
    def delete(self, emp_id):
        record = EmployeesRecord.query.filter_by(id=emp_id) \
            .first_or_404(description=f'Record with id={emp_id} is not available')
        db.session.delete(record)
        db.session.commit()
        return 'The record has been deleted'


class SearchEmployee(Resource):
    # to search for an employee by name
    @validate(search_types)
    @result_or_error
    def get(self):
        # collecting search data from the request
        search_args = search_parser.parse_args()
        records = EmployeesRecord.query.filter_by(last_name=search_args['last_name'],
                                                  first_name=search_args['first_name'],
                                                  father_name=search_args['father_name'])
        return [EmployeesRecord.serialize(record) for record in records]


api.add_resource(EmployeesRecordList, '/api/recordsAll', '/api', methods=['GET', 'POST'])
api.add_resource(Employee, '/api/record/<int:emp_id>', methods=['GET', 'PUT', 'DELETE'])
api.add_resource(SearchEmployee, '/api/search', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
