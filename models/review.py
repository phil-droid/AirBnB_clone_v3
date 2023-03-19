#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String

class Review(BaseModel):
    """ Review classto store review information """
    __tablename__='Review'
    
    place_id = Column(String(60), Foreignkey='places.id', nullable=False)
    user_id = Column(String(60), Foreignkey='users.id', nullable=False)
    text = Column(String(1024), nullable=False)
