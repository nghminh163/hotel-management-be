from flask import Blueprint, jsonify

from app.models.room import RoomType

mod = Blueprint('roomTypes', __name__, url_prefix='/roomTypes')


@mod.route('/', methods=['GET'])
def getRoomTypes():
    roomTypes: list[RoomType] = RoomType.query.all()
    return jsonify(list(map(lambda roomType: roomType.toJSON(), roomTypes)))

# getAvailableRoomByTypeId
