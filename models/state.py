#!/usr/bin/python3
""" State module"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base

class state(BaseModel, Base):
    __tablename__= 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")
