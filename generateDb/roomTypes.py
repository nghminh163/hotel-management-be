from app.models.room import RoomType
import json
from app import db
from app.models.service import Service


def generate():
    roomTypesData = json.load(
        open('generateDb/data/roomTypes.json'))
    roomTypes = map(lambda roomType: RoomType(
        area=roomType['area'],
        description=roomType['description'],
        price=roomType['price'],
        type=roomType['type'],
        promo=list(map(lambda x: Service.query.get(
            x), roomType['promoServices']))
    ), roomTypesData)
    db.session.add_all(roomTypes)
    db.session.commit()
