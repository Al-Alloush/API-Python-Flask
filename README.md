# API Python with Flask Framework
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