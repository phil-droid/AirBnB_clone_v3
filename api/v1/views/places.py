#!/usr/bin/python3
"""This module defines a new view for Place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, State, City, Amenity, Place


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for Place objects based on JSON request"""

    # Check if the request is valid JSON
    if not request.is_json:
        abort(400, description="Not a JSON")

    # Get the JSON body
    search_params = request.get_json()

    # Get the search parameters
    states = search_params.get('states', [])
    cities = search_params.get('cities', [])
    amenities = search_params.get('amenities', [])

    # Initialize the list of results
    results = []

    # Retrieve all Place objects if no search parameters are specified
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        for place in places:
            results.append(place.to_dict())

    else:
        # Retrieve all Place objects for each State id listed
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        if place not in results:
                            results.append(place.to_dict())

        # Retrieve all Place objects for each City id listed
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in results:
                        results.append(place.to_dict())

        # Filter the results based on the amenities list
        if amenities:
            amenities_objs = [storage.get(Amenity, amenity_id) for amenity_id in amenities]
            for place in results[:]:
                place_amenities = [storage.get(Amenity, amenity_id) for amenity_id in place.get('amenities', [])]
                if not all(amenity in place_amenities for amenity in amenities_objs):
                    results.remove(place)

    return jsonify(results)
