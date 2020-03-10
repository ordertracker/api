from app.database.db import db

class Organizations(db.Model):
    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }, 200

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    @classmethod
    def find_org_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all_organizations(cls):
        return cls.query.all()

    @classmethod
    def test(cls):
        return True
