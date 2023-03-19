#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage

class Place(BaseModel):
    """ A place to stay """

    __tablename__='places'
    
    city_id = Column(String(60), nullable=False, Foreignkey('cities.id'))
    user_id = Column(String(60), nullable=False, Foreignkey('users.id'))
    name = Column(String(128),nullable=False )
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []


   ''' represent a relationship with the class Review. If the Place object is deleted, all linked Review objects must be automatically deleted.'''
   reviews = relationship('Review', cascade="all, delete", backref="place")

   def reviews(self):
        """Getter attribute that returns the list of Review instances
        with place_id equals to the current Place.id
        """
         review_list = []
        all_reviews = storage.all(Review)
        for review in all_reviews.values():
            if review.place_id == self.id:
                review_list.append(review)
        return review_list
