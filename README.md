# API Python with Flask Framework
---
## Create user Class to Register and login, JWT, hash pass, uuid

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
## Create SQLite connection and create database


---
## create a virtual environment for a clean installation of Python and libraries in the machine.
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