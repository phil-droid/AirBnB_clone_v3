#!/usr/bin/python3

"""This module defines a class User"""

import hashlib
from models.base_model import BaseModel
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

class User(BaseModel):
    """This class defines a user by various attributes"""

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    _password = Column('password', String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)

    '''represent a relationship with the class Place. If the User object is deleted, all linked Place objects must be automatically deleted'''
    places = relationship("Place", cascade="all, delete", backref="user")

    '''represent a relationship with the clasReview. If the User object is deleted, all linked Review objects must be automatically deleted'''
    reviews = relationship('Review', cascade="all, delete", backref="user")

    def __init__(self, *args, **kwargs):
        """initializes a User object"""
        if kwargs.get('password'):
            self.password = kwargs['password']
            del kwargs['password']
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Getter for password"""
        return self._password

    @password.setter
    def password(self, pwd):
        """Setter for password"""
        self._password = hashlib.md5(pwd.encode()).hexdigest()

    def to_dict(self, **kwargs):
        """returns a dictionary representation of a User object"""
        if 'password' not in kwargs:
            d = dict(self.__dict__)
            del d['_sa_instance_state']
            d.pop('_password')
            return d
        else:
            return super().to_dict(**kwargs)
