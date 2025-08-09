from travel.config import db

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    country = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(50), unique=True, nullable=False)
    rating = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id":self.id,
            "country":self.country,
            "city":self.city,
            "rating":self.rating
        }
