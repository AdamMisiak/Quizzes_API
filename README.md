# Elevator simulation

Recruitment task for Backend Developer. Basic API to build and host quizzes. 


## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Contact](#contact)

## Technologies
* Django version: 4.1
* DRF version: 3.14.0
* Postgres version: 14.1

## Setup
To install make:
```
pip install make
```

To build containers:
```
make build
```

To start containers:
```
make up
```

To start containers in detach mode:
```
make up-detach
```

To migrate models:
```
make migrate
```

To create admin account:
```
make create-admin
Email: admin@admin.com
Password: admin
```

To init mock data:
```
make init-data
```

To run tests:
```
make test
```

To check swagger/docs:
```
http://localhost:8000/swagger/
http://localhost:8000/doc/
```

## Contact
Created by Adam Misiak
