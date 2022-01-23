# Alvin App Backend Test

Alvin app allows you automatically tracks your expenses and manages a budget for you based on your savings goals.

Main libraries used:
1. Flask-SQLAlchemy - adds support for SQLAlchemy ORM.
2. Flask-Marshmellow - object serialization/deserialization library.
3. Flask-JWT - for user authentication.


Project structure:
```
.
├── README.md
├── endpoints
│   ├── __init__.py
│   ├── transactions
│   │   ├── __init__.py
│   │   ├── model.py
│   │   └── resource.py
│   └── users
│       ├── __init__.py
│       ├── model.py
│       └── resource.py
├── requirements.txt
└── app.py
```

* endpoints - holds all endpoints.
* app.py - flask application initialization.

## Running 

1. Clone repository.
2. Create and activate a virtual environment by typing:

```
virtualenv venv
```

* then (for mac OS)

```
source venv/bin/activate
```

2. Install requirements by running:
```
pip install -r requirements.txt
```

3. Run following on your terminal to create the database:

```
python
```

```
from app import db
```

```
db.create_all()
```

4. Start server by running:
```
python app.py
```

## Usage
### User endpoint
POST http://127.0.0.1:5000/user (register user)

REQUEST
```json
{
    "name":"John Doe",
    "email":"test@tets.com",
    "password":"testpassword"
}
```
RESPONSE
```json
{
    "message": "user created successfully"
}
```
GET http://127.0.0.1:5000/api/users/1 (get a user)

RESPONSE
```json
{
    "user": {
        "admin": false,
        "email": "test@tets.com",
        "id": 1,
        "name": "John Doe"
    }
}
```

### Transaction endpoints

POST http://127.0.0.1:5000/transaction (create a transaction)

```json
{
    "amount":"545500",
    "category":"food",
    "description":"Five plates of pie",
    "merchant":"Village Market"
}
```

RESPONSE
```json
{
    "message": "transaction created successfully"
}
```

POST http://127.0.0.1:5000/transaction (get all transactions)

RESPONSE
```json
[
    {
        "amount": 545500.0,
        "category": "FOOD",
        "date": "2022-01-23T20:23:58.074211",
        "description": "Five plates of pie",
        "id": 1,
        "merchant": "Village Market",
        "user_id": 1
    }
]
```

GET http://127.0.0.1:5000/transaction/category/food/total/1 (amount per category per month i.e 1 = Jan)

RESPONSE
```json
{
    "category": "FOOD",
    "total": 545500.0
}
```

GET http://127.0.0.1:5000/transaction/category/food/total/period (amount per category per duration)

```json
{
    "start_date":"2022-01-22",
    "end_date":"2022-01-25"
}
```

RESPONCE
```json
{
    "category": "FOOD",
    "total": 545500.0
}
```

GET http://127.0.0.1:5000/transaction/total (total amount spent per category)

RESPONSE
```json
[
    {
        "category": "FOOD",
        "total": 545500.0
    },
    {
        "category": "ENTERTAINMENT",
        "total": 0
    },
    {
        "category": "TRANSPORT",
        "total": 0
    },
    {
        "category": "HEALTH",
        "total": 0
    },
    {
        "category": "SAVINGS",
        "total": 0
    },
    {
        "category": "EDUCATION",
        "total": 0
    },
    {
        "category": "FRIENDS_AND_FAMILY",
        "total": 145500.0
    },
    {
        "category": "OTHER",
        "total": 0
    }
]
```

More endpoints are on the shared Postman collection below:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/67636226f63648afc9db?action=collection%2Fimport)