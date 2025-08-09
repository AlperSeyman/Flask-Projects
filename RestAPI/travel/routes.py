from flask import Blueprint, jsonify, request
from .models import Destination
from .config import db


main = Blueprint('routes', __name__)

@main.route('/')
def home():

    return jsonify({"message":"Welcomte to the Travel API"})
    
# https://www.travelbook/destinations
@main.route('/destinations', methods=["GET"])
def get_destination():

    destinations = Destination.query.all()
    all_destination = []

    for d in destinations:
        all_destination.append(d.to_dict()) 

    return jsonify({"destination":all_destination})
    

# https://www.travelbook/destination/2
@main.route('/destinations/<int:id>', methods=["GET"])
def get_by_id(id):

    destination = Destination.query.get(id)

    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error":"Destination not found"}), 404


@main.route('/destinations', methods=["POST"])
def add_destination():

    data = request.get_json()

    new_destination = Destination(country=data["country"],
                                  city=data["city"],
                                  rating=data["rating"])
    
    db.session.add(new_destination)
    db.session.commit()

    return jsonify(new_destination.to_dict()), 201


@main.route('/destinations/<int:id>', methods=["PATCH"])
def update_destination(id):

    data = request.get_json()

    destination = Destination.query.get(id)

    if destination:
        
        updatable_fields = ["country", "city", "rating"]
        for field in updatable_fields:
            if field in data:
                setattr(destination, field ,data[field])


        db.session.commit()

        return jsonify(destination.to_dict())
    
    else:
        return jsonify({"error": "Destination not found"}), 404
    

@main.route('/destinations/<int:id>', methods=["DELETE"])
def delete_destination(id):

    destination = Destination.query.get(id)
    if destination:

        db.session.delete(destination)
        db.session.commit()

        return jsonify({"message":"Destination was deleted"}), 200
    
    else:
        return jsonify({"error":"Destination not found"}),404