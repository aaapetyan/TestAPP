# TestAPP
This project shows the implementation of the API web service. 
The API is written using Flask-RESTful, the database is built using SQLAlchemy.

## Running

### Install necessary packages
	pip install requirements.txt
	
### Create the database
	python db_creation.py
	
### Run the app
	flask run
	
## Usage
The web service contains a database of employees.

### Get full list of employees
`GET /api`

	curl http://127.0.0.1:5000/api
	
Response:

	{"result": [{"last_name": "Ivanov", "first_name": "Ivan", "father_name": "Ivanovich", "birth_year": 1985, "id": 1, "salary": 100.0, "position": "junior", "legal_name": "OOO TestApp", "department": "frontend"}, {"last_name": "Petrov", "first_name": "Petr", "father_name": "Petrovich", "birth_year": 1970, "id": 2, "salary": 500.0, "position": "lead", "legal_name": "OOO TestApp", "department": "backend"}, {"last_name": "Doe", "first_name": "John", "father_name": "Smith", "birth_year": 1990, "id": 3, "salary": 222.2, "position": "designer", "legal_name": "OOO OtherTestApp", "department": "marketing"}]}
	
### Add an employee
`POST /api`

	curl -X POST -H 'Content-Type: application/json' -d '{"last_name": "Apetyan", "first_name": "Arina", "father_name": "Arturovna", "birth_year": 1994, "id": 23, "salary": 100, "position": "intern", "legal_name": "OOO", "department": "backend"}' http://127.0.0.1:5000/api
	
Response:
	
	{"result": {"last_name": "Apetyan", "first_name": "Arina", "father_name": "Arturovna", "birth_year": 1994, "id": 23, "salary": 100.0, "position": "intern", "legal_name": "OOO", "department": "backend"}}
	
Adding an employee with already existing id:

	curl -X POST -H 'Content-Type: application/json' -d '{"last_name": "Apetyan", "first_name": "Arina", "father_name": "Arturovna", "birth_year": 1994, "id": 2, "salary": 100, "position": "intern", "legal_name": "OOO", "department": "backend"}' http://127.0.0.1:5000/api
	
Response:

	{"error": "no exception for 'Record with id=2 already exists'"}
	
Missing data (no "department"):

	curl -X POST -H 'Content-Type: application/json' -d '{"last_name": "Apetyan", "first_name": "Arina", "father_name": "Arturovna", "birth_year": 1994, "id": 23, "salary": 100, "position": "intern", "legal_name": "OOO"}' http://127.0.0.1:5000/api

Response:

	{"error": "department is missing"}
	
	
### Update the record for the employee

`PUT /api/record/{id}`

	curl -X PUT -H 'Content-Type: application/json' -d '{"last_name": "Apetyan", "first_name": "Arina", "father_name": "Arturovna", "birth_year": 1994, "id": 23, "salary": 100, "position": "junior", "legal_name": "OOO", "department": "backend"}' http://127.0.0.1:5000/api/record/23
	
Response:

	{"result": {"last_name": "Apetyan", "first_name": "Arina", "father_name": "Arturovna", "birth_year": 1994, "id": 23, "salary": 100.0, "position": "junior", "legal_name": "OOO", "department": "backend"}}

Trying to update non-existent record:

	curl -X PUT -H 'Content-Type: application/json' -d '{"last_name": "Apetyan", "first_name": "Arina", "father_name": "Arturovna", "birth_year": 1994, "id": 23, "salary": 100, "position": "junior", "legal_name": "OOO", "department": "backend"}' http://127.0.0.1:5000/api/record/100

Response:

	{"error": "404 Not Found: Record with id=100 is not available"}

### Delete the record for the employee

`DELETE /api/record/{id}`

	curl -X DELETE http://127.0.0.1:5000/api/record/23
	
Response:

	{"result": "The record has been deleted"}
	
Trying to delete non-existent record:

	curl -X DELETE http://127.0.0.1:5000/api/record/100
	
Response:

	{"error": "404 Not Found: Record with id=100 is not available"}

	
### Search for the employee
Searh by id:
`GET /api/record/{id}`

	curl http://127.0.0.1:5000/api/record/1
	
Response:

	{"result": {"last_name": "Ivanov", "first_name": "Ivan", "father_name": "Ivanovich", "birth_year": 1985, "id": 1, "salary": 100.0, "position": "junior", "legal_name": "OOO TestApp", "department": "frontend"}}
	
Searh by non-existent id:

	curl http://127.0.0.1:5000/api/record/100
	
Response:

	{"error": "404 Not Found: Record with id=100 is not available"}

Search by full name:
`GET /api/search`

	curl http://127.0.0.1:5000/api/search -X GET -H 'Content-Type: application/json' -d '{"last_name": "Ivanov", "fist_name": "Ivan", "father_name": "Ivanovich"}'
	
Response:

	{"result": {"last_name": "Ivanov", "first_name": "Ivan", "father_name": "Ivanovich", "birth_year": 1985, "id": 1, "salary": 100.0, "position": "junior", "legal_name": "OOO TestApp", "department": "frontend"}}
	
Search by full name (no such employee):

	curl http://127.0.0.1:5000/api/search -X GET -H 'Content-Type: application/json' -d '{"last_name": "Ivanov", "fist_name": "Petr", "father_name": "Petrovich"}'
	
Response:
	
	{"result: []}
	
Search by name ("last_name" is missing):

	curl http://127.0.0.1:5000/api/search -X GET -H 'Content-Type: application/json' -d '{"fist_name": "Ivan", "father_name": "Ivanovich"}'
	
Response:

	{"error": "last_name is missing"}

