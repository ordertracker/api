from app.database.db import db

class RoleModel(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80))
    name = db.Column(db.String(80))

    def __init__(self, key, name):
        self.key = key
        self.name = name

    def json(self):
        return {
            "id": self.id,
            "key": self.key,
            "name": self.name
        }, 200

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_role_by_key(cls, key):
        return cls.query.filter_by(key=key).first()
