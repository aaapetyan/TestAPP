from app import db
from app import EmployeesRecord

db.create_all()
first_record = EmployeesRecord(last_name='Ivanov', first_name='Ivan', father_name='Ivanovich',
                               birth_year=1985, id=1, salary=100.0, position='junior',
                               legal_name='OOO TestApp', department='frontend')
second_record = EmployeesRecord(last_name='Petrov', first_name='Petr', father_name='Petrovich',
                                birth_year=1970, id=2, salary=500.0, position='lead',
                                legal_name='OOO TestApp', department='backend')
third_record = EmployeesRecord(last_name='Doe', first_name='John', father_name='Smith',
                               birth_year=1990, id=3, salary=222.2, position='designer',
                               legal_name='OOO OtherTestApp', department='marketing')

db.session.add(first_record)
db.session.add(second_record)
db.session.add(third_record)
db.session.commit()

EmployeesRecord.query.all()
