from app.database.db import db

from flask import current_app as app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False, server_default='')
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    roles = db.relationship('Role', backref='user', lazy='dynamic')

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email
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

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }, 200

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_role_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

