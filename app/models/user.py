import hashlib
from sqlalchemy import ForeignKey
from sqlalchemy.orm.exc import NoResultFound

from app import db


class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, username, password, firstName, lastName):
        self.username = username
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.firstName = firstName
        self.lastName = lastName

    def __repr__(self):
        return '<User %s>' % self.title

    @classmethod
    def get(cls, user_id):
        try:
            return User.query.filter_by(id=user_id).one()
        except NoResultFound:
            return None

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
        }
