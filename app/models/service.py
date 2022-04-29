from sqlalchemy.orm.exc import NoResultFound

from app import db

class Service(db.Model):
    __tablename__ = 'Services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __init__(self, title, description, price):
        self.title = title
        self.description = description
        self.price = price

    def __repr__(self):
        return '<Service %s>' % self.title

    @classmethod
    def get(cls, service_id):
        try:
            return Service.query.filter_by(id=service_id).one()
        except NoResultFound:
            return None

    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
        }
