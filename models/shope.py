from db_sql_alchemy import db


class ShopeModel(db.Model):
    __tablename__ = 'shopes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()