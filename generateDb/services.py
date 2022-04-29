from app.models.service import Service
import json
from app import db

def generate():
    servicesData = json.load(
        open('generateDb/data/services.json'))
    services = map(lambda service: Service(title=service['title'],
                                           description=service['description'],
                                           price=service['price']
                                           ), servicesData)
    db.session.add_all(services)
    db.session.commit()
