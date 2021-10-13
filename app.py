from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
from flask_sqlalchemy import SQLAlchemy

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


parser = reqparse.RequestParser()
parser.add_argument('last_name', type=str, required=True, help='last_name is a required parameter!')
parser.add_argument('first_name', type=str, required=True)
parser.add_argument('father_name', type=str, required=True)
parser.add_argument('birth_year', type=int, required=True)
parser.add_argument('id', type=int, required=True)
parser.add_argument('salary', type=float, required=True)
parser.add_argument('position', type=str, required=True)
parser.add_argument('legal_name', type=str, required=True)
parser.add_argument('department', type=str, required=True)


class EmployeesRecordList(Resource):
    # to get the full list of employees
    def get(self):
        records = EmployeesRecord.query.all()
        return [EmployeesRecord.serialize(record) for record in records]

    # to add a new employee to the list
    def post(self):
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
        db.session.add(employee_record)
        db.session.commit()
        return EmployeesRecord.serialize(employee_record), 201


class Employee(Resource):
    # to search for the employee by id
    def get(self, emp_id):
        return EmployeesRecord.serialize(
            EmployeesRecord.query.filter_by(id=emp_id)
            .first_or_404(description=f'Record with id={emp_id} is not available'))

    # to update the information for the existing employee
    def put(self, emp_id):
        args = parser.parse_args()
        record = EmployeesRecord.query.filter_by(id=emp_id)\
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
        return EmployeesRecord.serialize(record), 201

    # to delete an employee from the list
    def delete(self, emp_id):
        record = EmployeesRecord.query.filter_by(id=emp_id)\
            .first_or_404(description=f'Record with id={emp_id} is not available')
        db.session.delete(record)
        db.session.commit()
        return '', 204


class SearchEmployee(Resource):
    # to search for an employee by name
    def get(self):
        last = request.args.get('last')
        first = request.args.get('first')
        father = request.args.get('father')
        records = EmployeesRecord.query.filter_by(last_name=last, first_name=first, father_name=father).all()
        return [EmployeesRecord.serialize(record) for record in records]


api.add_resource(EmployeesRecordList, '/recordsAll', '/')
api.add_resource(Employee, '/record/<int:emp_id>')
api.add_resource(SearchEmployee, '/search')

if __name__ == '__main__':
    app.run(debug=True)
