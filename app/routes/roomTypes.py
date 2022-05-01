from app.utils.roomType import getRoomsAvailableByRoomType
from flask import Blueprint, jsonify, request
from sqlalchemy import true
from app.models.booking import Booking
from random import shuffle

from app.models.room import Room, RoomType

mod = Blueprint('roomTypes', __name__, url_prefix='/roomTypes')


@mod.route('/', methods=['GET'])
def getRoomTypes():
    try:
        typeId = request.args.get('typeId', type=int)
        if typeId is None:
            roomTypes: list[RoomType] = RoomType.query.all()
            return jsonify({"isError":False, "data":list(map(lambda roomType: roomType.toJSON(), roomTypes))})
        else:
            roomType: RoomType = RoomType.query.get(typeId)
            if roomType is None:
                return jsonify({"isError": True, "msg": "Room type not found"})
            else:
                return jsonify({"isError":False, "data":roomType.toJSON(True)})
    except:
        return jsonify({"isError":True, "data":"Something went wrong"})

@mod.route('/getAvailable', methods=['GET'])
def getAvailableRoomByTypeId():
    typeId = request.args.get('typeId', default=0, type=int)
    availableRoomsRes = getRoomsAvailableByRoomType(typeId)
    if availableRoomsRes['isError'] is True:
        return jsonify(availableRoomsRes)
    else:
        availableRooms = availableRoomsRes['data']
        if len(availableRooms) > 0:
            return jsonify({"isError": False, "data": len(availableRooms)})
        else:
            return jsonify({"isError": True, "msg": "No room available"})
