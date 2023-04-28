#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                        self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

        def get(self, cls, id):
            """Retrieve an object based on class name and ID"""
            filename = "{}.{}".format(cls.__name__, id)
            objects = self.all(cls)
            return objects.get(filename)

        def count(self, cls=None):
            """Count the number of objects in storage"""
            if cls:
                objects = self.all(cls)
                return len(objects)
            else:
                objects = self.all()
                return len(objects)

        def list_amenities_of_place(self, place_id):
        """Retrieves the list of all Amenity objects of a Place"""
        place = self.get(Place, place_id)
        if not place:
            return None
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return amenities

    def delete_amenity_from_place(self, place_id, amenity_id):
        """Deletes a Amenity object to a Place"""
        place = self.get(Place, place_id)
        if not place:
            return None
        amenity = self.get(Amenity, amenity_id)
        if not amenity:
            return None
        if amenity not in place.amenities:
            return None
        place.amenities.remove(amenity)
        self.save()
        return {}

    def link_amenity_to_place
