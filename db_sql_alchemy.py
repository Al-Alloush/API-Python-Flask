from flask_sqlalchemy import SQLAlchemy

# create an object from SQLAlchemy to link to flask app,
# to look at all of the objects, that we tell it to, 
# then allowing us to map those objects to rows in a database. like insert, update,...
db = SQLAlchemy()