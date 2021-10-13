from app import db
from app import EmployeesRecord

db.create_all()
first_record = EmployeesRecord(last_name='Ivanov', first_name='Ivan', father_name='Ivanovich',
                               birth_year=1985, id=1, salary=100500.0, position='backend',
                               legal_name='OOO AAA', department='sales')
second_record = EmployeesRecord(last_name='Petrov', first_name='Petr', father_name='Petrovich',
                                birth_year=1970, id=2, salary=500100.0, position='frontend',
                                legal_name='OOO BBB', department='marketing')
third_record = EmployeesRecord(last_name='Pugacheva', first_name='Alla', father_name='Borisovna',
                               birth_year=1965, id=3, salary=5.5, position='lead singer',
                               legal_name='Iceberg', department='stage')
fourth_record = EmployeesRecord(last_name='Pugacheva', first_name='Alla', father_name='Borisovna',
                                birth_year=1965, id=4, salary=500.5, position='artist',
                                legal_name='Very Cold Iceberg', department='stage')

db.session.add(first_record)
db.session.add(second_record)
db.session.add(third_record)
db.session.add(fourth_record)
db.session.commit()

EmployeesRecord.query.all()
