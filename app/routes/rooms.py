from flask import Blueprint, jsonify

from app.models.room import Room

mod = Blueprint('rooms', __name__, url_prefix='/rooms')


@mod.route('/', methods=['GET'])
def getRooms():
    rooms: list[Room] = Room.query.all()
    return jsonify({"isError": False, "data": list(map(lambda room: room.toJSON(), rooms))})

@mod.route('/<room_id>', methods=['GET'])
def getRoomByNumber(room_id):
    room: Room = Room.query.get(room_id)
    return jsonify(room.toJSON())


