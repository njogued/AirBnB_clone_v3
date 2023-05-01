#!/usr/bin/python3
"""Index file"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON of status when queried"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def display_stats():
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    clss_stats = {}
    for key, value in classes.items():
        clss_stats[key] = storage.count(value)
    return jsonify(clss_stats)
