#!/usr/bin/python3

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """
    This class manages storage of hbnb models in MySQL database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        This method initializes a new instance of the DBStorage class by creating the engine and linking it to the MySQL database and user.
        """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', default='localhost')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}', pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        This method queries the current database session for all objects of a given class or all objects if no class is specified.
        """
        from models import classes
        objects = {}
        if cls is None:
            for c in classes:
                query_result = self.__session.query(c).all()
                for obj in query_result:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    objects[key] = obj
        else:
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = f'{obj.__class__.__name__}.{obj.id}'
                objects[key] = obj
        return objects

    def new(self, obj):
        """
        This method adds the object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        This method commits all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        This method deletes an object from the current database session.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        This method creates all tables in the database and creates the current database session from the engine.
        """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def get(self, cls, id):
        """Retrieve an object based on class name and ID"""
        key = "{}.{}".format(cls.__name__, id)
        return self.__session.query(cls).get(key)

    def count(self, cls=None):
         """Count the number of objects in storage"""
         if cls:
             return self.__session.query(cls).count()
          else:
              count = 0
              for cls in self.__classes:
                  count += self.__session.query(cls).count()
              return count
