from flask import Blueprint, jsonify, request
from sqlalchemy import true
from app.models.booking import Booking
from random import shuffle

from app.models.room import Room, RoomType

mod = Blueprint('roomTypes', __name__, url_prefix='/roomTypes')


@mod.route('/', methods=['GET'])
def getRoomTypes():
    roomTypes: list[RoomType] = RoomType.query.all()
    return jsonify(list(map(lambda roomType: roomType.toJSON(), roomTypes)))


@mod.route('/getAvailable', methods=['GET'])
def getAvailableRoomByTypeId():
    typeId = request.args.get('typeId', default=0, type=int)
    roomType: RoomType = RoomType.query.get(typeId)
    if roomType is None:
        return jsonify({"isError": True, "msg": "Room type not found"})
    rooms: list[Room] = Room.query.filter_by(
        roomType=roomType).all()  # Room for roomtype
    bookings = Booking.query.filter(Booking.status.in_([1, 2]),
                                    Booking.roomNumber.in_(list(map(lambda room: room.roomNumber, rooms)))).all()
    roomUsed = list(map(lambda booking: booking.roomNumber, bookings))
    roomAvailable = []
    for room in rooms:
        if room.roomNumber not in roomUsed:
            roomAvailable.append(room)
    if len(roomAvailable) > 0:
        return jsonify({"isError": False, "data": roomAvailable[0].toJSON(true)})
    else:
        return jsonify({"isError": True, "msg": "No room available"})