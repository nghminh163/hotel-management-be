from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound


from app import db

Base = declarative_base()


class Room(db.Model):
    __tablename__ = 'Rooms'
    roomNumber = db.Column(db.Integer, primary_key=True)
    roomType_id = db.Column(db.Integer, ForeignKey('RoomTypes.id'))
    roomType = db.relationship("RoomType")

    def __init__(self, roomNumber, roomType):
        self.roomNumber = roomNumber
        self.roomType = roomType

    def __repr__(self):
        return '<Room %s>' % self.roomNumber

    @classmethod
    def get(cls, room_number):
        try:
            return Room.query.filter_by(id=room_number).one()
        except NoResultFound:
            return None

    def toJSON(self):
        return {
            'roomNumber': self.roomNumber,
            'roomType': self.roomType
        }


RoomType_Service = db.Table('RoomType_Service',
                            db.Column('roomType_id', db.Integer,
                                      db.ForeignKey('RoomTypes.id')),
                            db.Column('service_id', db.Integer,
                                      db.ForeignKey('Services.id'))
                            )


class RoomType(db.Model):
    __tablename__ = 'RoomTypes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(30), nullable=False)
    area = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    promo = db.relationship("Service",
                            secondary=RoomType_Service)

    def __init__(self, type, area, description, price, promo):
        self.type = type
        self.area = area
        self.description = description
        self.price = price
        self.promo = promo

    def __repr__(self):
        return '<Roomtype %s>' % self.type

    @classmethod
    def get(cls, roomType_id):
        try:
            return RoomType.query.filter_by(id=roomType_id).one()
        except NoResultFound:
            return None

    def toJSON(self):
        return {
            "id": self.id,
            "type": self.type,
            "area": self.area,
            "description": self.description,
            "price": self.price,
            "promo": list(map(lambda x: x.toJSON(), self.promo))
        }
