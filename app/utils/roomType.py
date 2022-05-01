from app.models.booking import Booking
from app.models.room import Room, RoomType
def getRoomsAvailableByRoomType(roomType:int) -> dict:
    roomType: RoomType = RoomType.query.get(roomType)
    if roomType is None:
        return {"isError": True, "msg": "Room type not found"}
    rooms: list[Room] = Room.query.filter_by(
        roomType=roomType).all()  # Room for roomtype
    bookings = Booking.query.filter(Booking.status.in_([1, 2]),
                                    Booking.roomNumber.in_(list(map(lambda room: room.roomNumber, rooms)))).all()
    roomUsed = list(map(lambda booking: booking.roomNumber, bookings))
    roomAvailable = []
    for room in rooms:
        if room.roomNumber not in roomUsed:
            roomAvailable.append(room)
    return {"isError": False, "data": roomAvailable}
