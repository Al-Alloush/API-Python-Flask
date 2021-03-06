from db_sql_alchemy import db


class ShopeModel(db.Model):
    __tablename__ = 'shopes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # lazy=dynamic is to avoid expensive operation to create an object for each item in a database that matches that shope id.
    products = db.relationship('ProductModel', lazy='dynamic')


    def __init__(self, name):
        self.name = name

    def json(self):
        '''
        with lazy equals dynamic, self.products no longer is a list of products, 
        now it is a query builder that has the ability to look into the Products table, 
        then use .all() to retrieve all of the Product in that table.'''
        return {'id': self.id, 'name': self.name, 'items': [product.json() for product in self.products.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()