from db_sql_alchemy import db

class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))
    shope_id = db.Column(db.Integer, db.ForeignKey('shopes.id'))
    shope = db.relationship('ShopeModel')

    
    def __init__(self, name, price, shope_id):
        self.name = name
        self.price = price
        self.shope_id = shope_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'shope':self.shope_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()