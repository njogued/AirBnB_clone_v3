#!/usr/bin/python3
"""An app"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_all(exception=None):
    """A method that calls storage.close()
    Not specified in instruction but tear_all must have
    one argument, else TypeError"""
    storage.close()


@app.errorhandler(404)
def handle_404(e):
    """Function to handle 404 error with a JSON formatted message"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, port, threaded=True)
