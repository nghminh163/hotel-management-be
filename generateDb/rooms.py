from app.models.room import Room, RoomType
import json
from app import db


def generate():
    roomsData = json.load(
        open('generateDb/data/rooms.json'))
    rooms = map(lambda room: Room(
        roomNumber=room['roomNumber'],
        roomType=RoomType.query.get(
            room['typeId'])
    ), roomsData)

    db.session.add_all(rooms)
    db.session.commit()
