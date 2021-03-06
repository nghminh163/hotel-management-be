from datetime import datetime
from email.policy import default
from sqlalchemy import ForeignKey
from sqlalchemy.orm.exc import NoResultFound

from app import db


class Booking(db.Model):
    __tablename__ = 'Bookings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clientName = db.Column(db.String(255), nullable=False)
    clientNumber = db.Column(db.String(255), nullable=False)
    checkinDate = db.Column(db.String(30))
    checkoutDate = db.Column(db.String(30))
    checkinTime = db.Column(db.String(30))
    checkoutTime = db.Column(db.String(30))

    status = db.Column(db.Integer, default=1)
    roomNumber = db.Column(db.Integer, ForeignKey('Rooms.roomNumber'))
    room = db.relationship("Room")

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, clientName, clientNumber, checkinDate, checkoutDate, roomNumber, checkinTime="", checkoutTime="", status=1, created_at=db.func.now()):
        self.clientName = clientName
        self.clientNumber = clientNumber
        self.checkinDate = checkinDate
        self.checkoutDate = checkoutDate
        self.roomNumber = roomNumber

        self.checkinTime = checkinTime
        self.checkoutTime = checkoutTime
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        return '<Booking %s>' % self.id

    @classmethod
    def get(cls, service_id):
        try:
            return Booking.query.filter_by(id=service_id).one()
        except NoResultFound:
            return None

    def toJSON(self):
        return {
            'id': self.id,
            'clientName': self.clientName,
            'clientNumber': self.clientNumber,
            'checkinDate': self.checkinDate,
            'checkoutDate': self.checkoutDate,
            'status': self.status,
            'roomNumber': self.roomNumber,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
