#!/usr/bin/python3
"""Using HTTP methods for places"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'], strict_slashes=False)
def places_in_city(city_id):
    """Get and Post methods for places in city"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    if request.method == "GET":
        all_plcs = storage.all(Place)
        plcs = []
        for one in all_plcs.values():
            if one.city_id == city_id:
                plcs.append(one.to_dict())
        return jsonify(plcs)
    elif request.method == "POST":
        input_json = request.get_json()
        if not input_json:
            abort(400, "Not a JSON")
        if not input_json["user_id"]:
            abort(400, "Missing user_id")
        if not storage.get(User, input_json["user_id"]):
            abort(404)
        if not input_json["name"]:
            abort(400, "Missing name")
        new_place = Place(**input_json)
        new_place.save()
        return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def all_places(place_id):
    """Methods for places route"""
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    if request.method == "GET":
        return jsonify(place_obj.to_dict())
    elif request.method == "DELETE":
        place_obj.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        input_json = request.get_json()
        if not input_json:
            abort(400, "Not a JSON")
        for k, v in input_json.items():
            setattr(place_obj, k, v)
        place.save()
        return jsonify(place.to_dict()), 200
