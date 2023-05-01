#!/usr/bin/python3
"""Handling CRUD for cities"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def cities_in_state(state_id):
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    if request.method == "GET":
        city_objs = storage.all(City)
        cities = [city_obj.to_dict() for city_obj
                  in city_objs.values() if city_obj.state_id == state_id]
        return jsonify(cities)
    elif request.method == "POST":
        input_json = request.get_json()
        if not input_json:
            abort(404, 'Not a JSON')
        if not input_json["name"]:
            abort(400, 'Missing name')
        input_json["state_id"] = state_id
        new_city = City(**input_json)
        new_city.save()
        return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def one_city(city_id):
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    if request.method == "GET":
        return jsonify(city_obj.to_dict())
    elif request.method == "PUT":
        input_json = request.get_json()
        if not input_json:
           abortt(404, 'Not a JSON')
        city_obj.name = input_json["name"]
        city_obj.save()
        return jsonify(city_obj.to_dict()), 200
    elif request.method == "DELETE":
        city_obj.delete()
        storage.save()
        return jsonify({}), 200
