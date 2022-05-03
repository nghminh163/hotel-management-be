from app.models.user import User
import json
from app import db


def generate():
    usersData = json.load(
        open('generateDb/data/users.json'))
    users = map(lambda user: User(firstName=user['firstName'], lastName=user['lastName'],
                username=user['username'], password=user['password']), usersData)
    db.session.add_all(users)
    db.session.commit()
