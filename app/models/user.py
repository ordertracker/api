from app.database.db import db
from app.models.role import RoleModel

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String())
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    role = db.relationship("RoleModel", backref=(db.backref("roles", uselist=False)))

    def __init__(self, username, password, name, email, role_id):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.role_id = role_id

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "role_id": self.role_id
        }, 200

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()