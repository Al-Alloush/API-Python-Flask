# API Python with Flask Framework
---
## 6- add Product and Shope Models and thiere resources files


---
## 5- Add a Python SQL toolkit and Object Relational Mapper [(Flask SQLAlchemy)](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
**SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.**
- create a object from SQLAlchemy 
- extend Models the new SQLAlchemy object and set some info like table name, and so
- is in app.py specify a configuration property


---
## 4-  organised the files 
some folders in Python are called packages, and there's a minor difference between a package and a folder.

### create two folders 
- models        # A model is our internal representation of an entity.
- resources     # A resource is the external representation of an entity. API clients, like a website or a mobile app, think they're interacting with resources that's what they see. And when API responds it responds with resources.
to creat a backage in python 2.7 and earlier insted a folder need to add inside the folder ```__init__.py``` file, this file tells Python, that it can look inside these folders for Python files, but in Python 3.5 and leater it will most likely work.

---
## 3- Create user Class to Register and login, JWT, hash pass, uuid

- for user id use uuid (unique User ID) [page Link](https://docs.python.org/3/library/uuid.html)
```
>> import uuid
>> uuid.uuid4()
```
- hashing the password
- use JWT to authorize users, from flask_jwt library, this library provide a auth endpoint to Authorize users
```
http://0.0.0.0:5000/auth
this endpoit need two functions (authenticate and identity):
    - authenticate: to check if user exist and return the user
    - identity: to get the user id to add it in access token
```
- 




---
## 2- Create SQLite connection and create database


---
## 1- create a virtual environment for a clean installation of Python and libraries in the machine.
*note: in docker we don't need it, just when we install python in a local machine*



A virtual environment mimics reinstalling Python without libraries.

after install Python, install virtualelenv:
```
> pip install virtualenv
```
then :
```
> virtualenv <virtual name> --python=python<version>
```
then activate the new environment
```
Mac/Linux
> source <virtual name>/bin/activate
Windows:
> ./<virtual name>/Scripts/activate.bat
```

to get all Libraries has been installed in Python
````
pip<virsion> freeze
```