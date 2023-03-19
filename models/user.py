#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from sqlalchemy import string, Column

#user class

class User(BaseModel):
    """This class defines a user by various attributes"""

    __tablename__='users'
    
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    
    '''represent a relationship with the class Place. If the User object is deleted, all linked Place objects must be automatically deleted'''
    places = relationship("Place", cascade="all, delete", backref="user")
