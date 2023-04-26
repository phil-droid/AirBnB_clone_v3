#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Removes the current SQLAlchemy Session after each request.
    """
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays a HTML page like 8-index.html from the AirBnB clone - Web static project.
    """
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda amenity: amenity.name)
    places = sorted(storage.all(Place).values(), key=lambda place: place.name)
    cities = sorted(storage.all(City).values(), key=lambda city: city.name)
    return render_template('100-hbnb.html', states=states, amenities=amenities, places=places, cities=cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
