#!/usr/bin/python3
"""This module defines a variable storage"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """This class defines attributes and methods for a Database Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes instance of DBStorage"""
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        db = os.getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects"""
        objs = {}
        if cls is None:
            classes = [User, State, City, Amenity, Place, Review]
            for c in classes:
                for obj in self.__session.query(c):
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objs[key] = obj
        else:
            for obj in self.__session.query(cls):
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objs[key] = obj
        return objs

    def new(self, obj):
        """Adds a new object to the database"""
        self.__session.add(obj)

    def save(self):
        """Saves changes made to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
