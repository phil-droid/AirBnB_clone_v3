#!/usr/bin/python3

import hashlib
import os
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BaseModel:
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if key == 'password':
                self.password = self.__hash_password(value)
            else:
                setattr(self, key, value)

    def __hash_password(self, password):
        """Hashes a password using MD5 and a salt"""
        salt = os.urandom(32).hex()
        hashed_password = hashlib.md5((password + salt).encode()).hexdigest()
        return salt + hashed_password

    def verify_password(self, password):
        """Verifies a password against the hashed password"""
        salt = self.password[:64]
        hashed_password = hashlib.md5((password + salt).encode()).hexdigest()
        return self.password[64:] == hashed_password

    def save(self):
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        models.storage.delete(self)

    def to_dict(self, **kwargs):
        new_dict = {}
        for key, value in self.__dict__.items():
            if key == 'password' and 'password' not in kwargs:
                continue
            if key == '_sa_instance_state':
                continue
            new_dict[key] = value
        return new_dict
