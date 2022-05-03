from sqlalchemy import ForeignKey
from sqlalchemy.orm.exc import NoResultFound

from app import db


class Service(db.Model):
    __tablename__ = 'Services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, title, description, price):
        self.title = title
        self.description = description
        self.price = price

    def __repr__(self):
        return '<Service %s>' % self.title

    @classmethod
    def get(cls, service_id):
        try:
            return Service.query.filter_by(id=service_id).one()
        except NoResultFound:
            return None

    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
        }


class ServiceOrders(db.Model):
    __tablename__ = 'ServiceOrders'

    orderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer, default=1)
    booking_id = db.Column(db.Integer, ForeignKey('Bookings.id'))
    booking = db.relationship("Booking")
    service_id = db.Column(db.Integer, ForeignKey('Services.id'))
    service = db.relationship("Service")
    note = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self,  booking_id, service_id, note, status=1):
        self.status = status
        self.booking_id = booking_id
        self.service_id = service_id
        self.note = note

    def __repr__(self):
        return '<ServiceOrder %s>' % self.orderId

    @classmethod
    def get(cls, order_id):
        try:
            return ServiceOrders.query.filter_by(id=order_id).one()
        except NoResultFound:
            return None

    def toJSON(self):
        return {
            "status": self.status,
            "orderId": self.orderId,
            "bookingId": self.booking_id,
            "serviceId": self.service_id,
            "note": self.note,
            "createdAt": self.created_at.isoformat(),
            "roomNumber":self.booking.roomNumber
        }
